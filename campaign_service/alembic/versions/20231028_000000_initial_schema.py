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
    # Create campaigns table
    op.create_table(
        'campaigns',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('concept', sa.Text, nullable=False),
        sa.Column('theme', sa.String(100), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('version', sa.Integer, nullable=False, server_default='1'),
        sa.Column('status', sa.String(50), nullable=False, server_default='draft'),
        sa.Column('metadata', postgresql.JSONB, nullable=False, server_default='{}'),
    )

    # Create chapters table
    op.create_table(
        'chapters',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('campaign_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('campaigns.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('sequence_number', sa.Integer, nullable=False),
        sa.Column('theme', sa.String(100), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='draft'),
        sa.Column('metadata', postgresql.JSONB, nullable=False, server_default='{}'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
    )

    # Create campaign_versions table
    op.create_table(
        'campaign_versions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('campaign_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('campaigns.id', ondelete='CASCADE'), nullable=False),
        sa.Column('version_number', sa.Integer, nullable=False),
        sa.Column('state', postgresql.JSONB, nullable=False),
        sa.Column('message', sa.Text),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('created_by', postgresql.UUID(as_uuid=True)),
    )

    # Create campaign_participants table
    op.create_table(
        'campaign_participants',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('campaign_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('campaigns.id', ondelete='CASCADE'), nullable=False),
        sa.Column('character_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('metadata', postgresql.JSONB, nullable=False, server_default='{}'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
    )

    # Create indexes
    op.create_index('ix_campaigns_name', 'campaigns', ['name'])
    op.create_index('ix_campaigns_theme', 'campaigns', ['theme'])
    op.create_index('ix_campaigns_status', 'campaigns', ['status'])
    op.create_index('ix_chapters_campaign_id', 'chapters', ['campaign_id'])
    op.create_index('ix_chapters_sequence_number', 'chapters', ['sequence_number'])
    op.create_index('ix_chapters_status', 'chapters', ['status'])
    op.create_index('ix_campaign_versions_campaign_id', 'campaign_versions', ['campaign_id'])
    op.create_index('ix_campaign_versions_version_number', 'campaign_versions', ['version_number'])
    op.create_index('ix_campaign_participants_campaign_id', 'campaign_participants', ['campaign_id'])
    op.create_index('ix_campaign_participants_character_id', 'campaign_participants', ['character_id'])


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('campaign_participants')
    op.drop_table('campaign_versions')
    op.drop_table('chapters')
    op.drop_table('campaigns')