# Copyright (C) 2025 AIDC-AI
# This project is licensed under the MIT License (SPDX-License-identifier: MIT).

import os
import json
import uuid
from datetime import datetime
from typing import Optional, Any

import asyncpg
from pixelle.logger import logger


DATABASE_URL = os.getenv("DATABASE_URL")

_pool: Optional[asyncpg.Pool] = None


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        if not DATABASE_URL:
            raise RuntimeError("DATABASE_URL environment variable is not set")
        _pool = await asyncpg.create_pool(DATABASE_URL, min_size=2, max_size=10)
    return _pool


async def close_pool():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


def _json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


# ==================== MCP Workflows ====================

async def create_workflow(
    workspace_id: str,
    name: str,
    workflow: dict,
    description: str = "",
    is_template: bool = False,
) -> dict:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO mcp_workflows (workspace_id, name, workflow, description, is_template)
            VALUES ($1, $2, $3::jsonb, $4, $5)
            RETURNING id, workspace_id, name, workflow, description, is_template, created_at, updated_at
            """,
            workspace_id,
            name,
            json.dumps(workflow, default=_json_serial),
            description,
            is_template,
        )
        return dict(row)


async def get_workflow(workflow_id: str) -> Optional[dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM mcp_workflows WHERE id = $1",
            uuid.UUID(workflow_id),
        )
        return dict(row) if row else None


async def list_workflows(
    workspace_id: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        if workspace_id:
            rows = await conn.fetch(
                "SELECT * FROM mcp_workflows WHERE workspace_id = $1 ORDER BY created_at DESC LIMIT $2 OFFSET $3",
                workspace_id,
                limit,
                offset,
            )
        else:
            rows = await conn.fetch(
                "SELECT * FROM mcp_workflows ORDER BY created_at DESC LIMIT $1 OFFSET $2",
                limit,
                offset,
            )
        return [dict(r) for r in rows]


async def update_workflow(
    workflow_id: str,
    name: Optional[str] = None,
    workflow: Optional[dict] = None,
    description: Optional[str] = None,
    is_template: Optional[bool] = None,
) -> Optional[dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        sets = []
        args = []
        idx = 1
        if name is not None:
            sets.append(f"name = ${idx}")
            args.append(name)
            idx += 1
        if workflow is not None:
            sets.append(f"workflow = ${idx}::jsonb")
            args.append(json.dumps(workflow, default=_json_serial))
            idx += 1
        if description is not None:
            sets.append(f"description = ${idx}")
            args.append(description)
            idx += 1
        if is_template is not None:
            sets.append(f"is_template = ${idx}")
            args.append(is_template)
            idx += 1
        if not sets:
            return await get_workflow(workflow_id)

        args.append(uuid.UUID(workflow_id))
        sql = f"UPDATE mcp_workflows SET {', '.join(sets)} WHERE id = ${idx} RETURNING *"
        row = await conn.fetchrow(sql, *args)
        return dict(row) if row else None


async def delete_workflow(workflow_id: str) -> bool:
    pool = await get_pool()
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM mcp_workflows WHERE id = $1",
            uuid.UUID(workflow_id),
        )
        return result == "DELETE 1"


# ==================== MCP Tools ====================

async def create_tool(
    workflow_id: str,
    name: str,
    description: str = "",
    input_schema: dict = None,
    output_schema: dict = None,
    enabled: bool = True,
) -> dict:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO mcp_tools (workflow_id, name, description, input_schema, output_schema, enabled)
            VALUES ($1, $2, $3, $4::jsonb, $5::jsonb, $6)
            RETURNING *
            """,
            uuid.UUID(workflow_id),
            name,
            description,
            json.dumps(input_schema or {}, default=_json_serial),
            json.dumps(output_schema or {}, default=_json_serial),
            enabled,
        )
        return dict(row)


async def get_tool(tool_id: str) -> Optional[dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM mcp_tools WHERE id = $1",
            uuid.UUID(tool_id),
        )
        return dict(row) if row else None


async def list_tools(
    workflow_id: Optional[str] = None,
    enabled_only: bool = False,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        conditions = []
        args = []
        idx = 1

        if workflow_id:
            conditions.append(f"workflow_id = ${idx}")
            args.append(uuid.UUID(workflow_id))
            idx += 1
        if enabled_only:
            conditions.append(f"enabled = true")

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        args.extend([limit, offset])
        sql = f"SELECT * FROM mcp_tools {where} ORDER BY created_at DESC LIMIT ${idx} OFFSET ${idx + 1}"
        rows = await conn.fetch(sql, *args)
        return [dict(r) for r in rows]


async def update_tool(
    tool_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    input_schema: Optional[dict] = None,
    output_schema: Optional[dict] = None,
    enabled: Optional[bool] = None,
) -> Optional[dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        sets = []
        args = []
        idx = 1
        if name is not None:
            sets.append(f"name = ${idx}")
            args.append(name)
            idx += 1
        if description is not None:
            sets.append(f"description = ${idx}")
            args.append(description)
            idx += 1
        if input_schema is not None:
            sets.append(f"input_schema = ${idx}::jsonb")
            args.append(json.dumps(input_schema, default=_json_serial))
            idx += 1
        if output_schema is not None:
            sets.append(f"output_schema = ${idx}::jsonb")
            args.append(json.dumps(output_schema, default=_json_serial))
            idx += 1
        if enabled is not None:
            sets.append(f"enabled = ${idx}")
            args.append(enabled)
            idx += 1
        if not sets:
            return await get_tool(tool_id)

        args.append(uuid.UUID(tool_id))
        sql = f"UPDATE mcp_tools SET {', '.join(sets)} WHERE id = ${idx} RETURNING *"
        row = await conn.fetchrow(sql, *args)
        return dict(row) if row else None


async def delete_tool(tool_id: str) -> bool:
    pool = await get_pool()
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM mcp_tools WHERE id = $1",
            uuid.UUID(tool_id),
        )
        return result == "DELETE 1"


# ==================== MCP Executions ====================

async def create_execution(
    tool_id: str,
    input_data: dict = None,
    output_data: dict = None,
    status: str = "pending",
    error: Optional[str] = None,
    duration_ms: Optional[int] = None,
) -> dict:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO mcp_executions (tool_id, input, output, status, error, duration_ms)
            VALUES ($1, $2::jsonb, $3::jsonb, $4, $5, $6)
            RETURNING *
            """,
            uuid.UUID(tool_id),
            json.dumps(input_data or {}, default=_json_serial),
            json.dumps(output_data or {}, default=_json_serial),
            status,
            error,
            duration_ms,
        )
        return dict(row)


async def get_execution(execution_id: str) -> Optional[dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM mcp_executions WHERE id = $1",
            uuid.UUID(execution_id),
        )
        return dict(row) if row else None


async def list_executions(
    tool_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        conditions = []
        args = []
        idx = 1

        if tool_id:
            conditions.append(f"tool_id = ${idx}")
            args.append(uuid.UUID(tool_id))
            idx += 1
        if status:
            conditions.append(f"status = ${idx}")
            args.append(status)
            idx += 1

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        args.extend([limit, offset])
        sql = f"SELECT * FROM mcp_executions {where} ORDER BY created_at DESC LIMIT ${idx} OFFSET ${idx + 1}"
        rows = await conn.fetch(sql, *args)
        return [dict(r) for r in rows]


async def update_execution(
    execution_id: str,
    output_data: Optional[dict] = None,
    status: Optional[str] = None,
    error: Optional[str] = None,
    duration_ms: Optional[int] = None,
) -> Optional[dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        sets = []
        args = []
        idx = 1
        if output_data is not None:
            sets.append(f"output = ${idx}::jsonb")
            args.append(json.dumps(output_data, default=_json_serial))
            idx += 1
        if status is not None:
            sets.append(f"status = ${idx}")
            args.append(status)
            idx += 1
        if error is not None:
            sets.append(f"error = ${idx}")
            args.append(error)
            idx += 1
        if duration_ms is not None:
            sets.append(f"duration_ms = ${idx}")
            args.append(duration_ms)
            idx += 1
        if not sets:
            return await get_execution(execution_id)

        args.append(uuid.UUID(execution_id))
        sql = f"UPDATE mcp_executions SET {', '.join(sets)} WHERE id = ${idx} RETURNING *"
        row = await conn.fetchrow(sql, *args)
        return dict(row) if row else None


# ==================== File Registration ====================

async def register_file(
    workspace_id: str,
    service: str,
    file_type: str,
    file_name: str,
    file_path: str,
    file_size: Optional[int] = None,
    mime_type: Optional[str] = None,
    metadata: dict = None,
) -> dict:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO files (workspace_id, service, file_type, file_name, file_path, file_size, mime_type, metadata)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8::jsonb)
            RETURNING *
            """,
            workspace_id,
            service,
            file_type,
            file_name,
            file_path,
            file_size,
            mime_type,
            json.dumps(metadata or {}, default=_json_serial),
        )
        return dict(row)


async def get_file(file_id: str) -> Optional[dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM files WHERE id = $1",
            uuid.UUID(file_id),
        )
        return dict(row) if row else None


async def list_files(
    workspace_id: Optional[str] = None,
    service: Optional[str] = None,
    file_type: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        conditions = []
        args = []
        idx = 1

        if workspace_id:
            conditions.append(f"workspace_id = ${idx}")
            args.append(workspace_id)
            idx += 1
        if service:
            conditions.append(f"service = ${idx}")
            args.append(service)
            idx += 1
        if file_type:
            conditions.append(f"file_type = ${idx}")
            args.append(file_type)
            idx += 1

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        args.extend([limit, offset])
        sql = f"SELECT * FROM files {where} ORDER BY created_at DESC LIMIT ${idx} OFFSET ${idx + 1}"
        rows = await conn.fetch(sql, *args)
        return [dict(r) for r in rows]


async def delete_file(file_id: str) -> bool:
    pool = await get_pool()
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM files WHERE id = $1",
            uuid.UUID(file_id),
        )
        return result == "DELETE 1"


# ==================== Activity Logging ====================

async def log_activity(
    service: str,
    action: str,
    workspace_id: Optional[str] = None,
    user_id: Optional[str] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    details: dict = None,
    ip_address: Optional[str] = None,
) -> dict:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO activity_logs (workspace_id, user_id, service, action, resource_type, resource_id, details, ip_address)
            VALUES ($1, $2, $3, $4, $5, $6, $7::jsonb, $8::inet)
            RETURNING *
            """,
            workspace_id,
            user_id,
            service,
            action,
            resource_type,
            resource_id,
            json.dumps(details or {}, default=_json_serial),
            ip_address,
        )
        return dict(row)


async def list_activity_logs(
    workspace_id: Optional[str] = None,
    service: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        conditions = []
        args = []
        idx = 1

        if workspace_id:
            conditions.append(f"workspace_id = ${idx}")
            args.append(workspace_id)
            idx += 1
        if service:
            conditions.append(f"service = ${idx}")
            args.append(service)
            idx += 1

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        args.extend([limit, offset])
        sql = f"SELECT * FROM activity_logs {where} ORDER BY created_at DESC LIMIT ${idx} OFFSET ${idx + 1}"
        rows = await conn.fetch(sql, *args)
        return [dict(r) for r in rows]


# ==================== Error Logging ====================

async def log_error(
    service: str,
    message: str,
    level: str = "error",
    stack_trace: Optional[str] = None,
    context: dict = None,
) -> dict:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO error_logs (service, level, message, stack_trace, context)
            VALUES ($1, $2, $3, $4, $5::jsonb)
            RETURNING *
            """,
            service,
            level,
            message,
            stack_trace,
            json.dumps(context or {}, default=_json_serial),
        )
        return dict(row)


# ==================== Health Check ====================

async def check_connection() -> bool:
    try:
        pool = await get_pool()
        async with pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False
