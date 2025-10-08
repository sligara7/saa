"""Initial schema

Revision ID: 20231028_000000
Revises: 
Create Date: 2023-10-28 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20231028_000000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create generation_requests table
    op.create_table(
        'generation_requests',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('prompt', sa.Text, nullable=False),
        sa.Column('context', postgresql.JSONB, nullable=False, server_default='{}'),
        sa.Column('model', sa.String(50), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('completed_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('tokens_used', sa.Integer),
        sa.Column('status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('error_message', sa.Text),
        sa.Column('metadata', postgresql.JSONB, nullable=False, server_default='{}')
    )

    # Create response_cache table
    op.create_table(
        'response_cache',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('cache_key', sa.String(255), nullable=False, unique=True),
        sa.Column('response', sa.Text, nullable=False),
        sa.Column('prompt', sa.Text, nullable=False),
        sa.Column('model', sa.String(50), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('expires_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('metadata', postgresql.JSONB, nullable=False, server_default='{}')
    )

    # Create rate_limits table
    op.create_table(
        'rate_limits',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('model', sa.String(50), nullable=False),
        sa.Column('tokens_used', sa.Integer, nullable=False, server_default='0'),
        sa.Column('last_request', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('reset_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('metadata', postgresql.JSONB, nullable=False, server_default='{}')
    )

    # Create prompt_templates table
    op.create_table(
        'prompt_templates',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('name', sa.String(100), nullable=False, unique=True),
        sa.Column('template', sa.Text, nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('parameters', postgresql.JSONB, nullable=False, server_default='[]'),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('version', sa.Integer, nullable=False, server_default='1'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('metadata', postgresql.JSONB, nullable=False, server_default='{}')
    )

    # Create indexes
    op.create_index('ix_generation_requests_model', 'generation_requests', ['model'])
    op.create_index('ix_generation_requests_user_id', 'generation_requests', ['user_id'])
    op.create_index('ix_generation_requests_status', 'generation_requests', ['status'])
    op.create_index('ix_generation_requests_created_at', 'generation_requests', ['created_at'])
    op.create_index('ix_response_cache_cache_key', 'response_cache', ['cache_key'])
    op.create_index('ix_response_cache_model', 'response_cache', ['model'])
    op.create_index('ix_response_cache_expires_at', 'response_cache', ['expires_at'])
    op.create_index('ix_rate_limits_user_id_model', 'rate_limits', ['user_id', 'model'])
    op.create_index('ix_rate_limits_reset_at', 'rate_limits', ['reset_at'])
    op.create_index('ix_prompt_templates_name', 'prompt_templates', ['name'])
    op.create_index('ix_prompt_templates_category', 'prompt_templates', ['category'])


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('prompt_templates')
    op.drop_table('rate_limits')
    op.drop_table('response_cache')
    op.drop_table('generation_requests')