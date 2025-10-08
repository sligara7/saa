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
    # Create images table
    op.create_table(
        'images',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('storage_path', sa.String(255), nullable=False),
        sa.Column('content_type', sa.String(50), nullable=False),
        sa.Column('size_bytes', sa.Integer, nullable=False),
        sa.Column('width', sa.Integer, nullable=False),
        sa.Column('height', sa.Integer, nullable=False),
        sa.Column('format', sa.String(10), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('metadata', postgresql.JSONB, nullable=False, server_default='{}'),
        sa.Column('status', sa.String(50), nullable=False, server_default='active'),
        sa.Column('tags', postgresql.ARRAY(sa.Text), nullable=False, server_default='{}')
    )

    # Create generation_jobs table
    op.create_table(
        'generation_jobs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('prompt', sa.Text, nullable=False),
        sa.Column('parameters', postgresql.JSONB, nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('started_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('completed_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('result_image_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('images.id')),
        sa.Column('error_message', sa.Text),
        sa.Column('metadata', postgresql.JSONB, nullable=False, server_default='{}')
    )

    # Create image_versions table
    op.create_table(
        'image_versions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('image_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('images.id', ondelete='CASCADE'), nullable=False),
        sa.Column('version_number', sa.Integer, nullable=False),
        sa.Column('storage_path', sa.String(255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('metadata', postgresql.JSONB, nullable=False, server_default='{}')
    )

    # Create indexes
    op.create_index('ix_images_content_type', 'images', ['content_type'])
    op.create_index('ix_images_status', 'images', ['status'])
    op.create_index('ix_images_created_at', 'images', ['created_at'])
    op.create_index('ix_generation_jobs_status', 'generation_jobs', ['status'])
    op.create_index('ix_generation_jobs_started_at', 'generation_jobs', ['started_at'])
    op.create_index('ix_image_versions_image_id', 'image_versions', ['image_id'])
    op.create_index('ix_image_versions_version_number', 'image_versions', ['version_number'])


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('image_versions')
    op.drop_table('generation_jobs')
    op.drop_table('images')