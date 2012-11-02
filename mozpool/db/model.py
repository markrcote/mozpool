# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sqlalchemy as sa

metadata = sa.MetaData()

boards = sa.Table('boards', metadata,
    sa.Column('id', sa.Integer(unsigned=True), primary_key=True, nullable=False),
    sa.Column('name', sa.String(32), nullable=False),
    sa.Column('fqdn', sa.String(256), nullable=False),
    sa.Column('inventory_id', sa.Integer(unsigned=True), nullable=False),
    sa.Column('status', sa.String(32), nullable=False),
    sa.Column('mac_address', sa.String(12), nullable=False),
    sa.Column('imaging_server_id', sa.Integer(unsigned=True),
        sa.ForeignKey('imaging_servers.id', ondelete='RESTRICT'),
        nullable=False),
    sa.Column('relay_info', sa.Text),
    sa.Column('boot_config', sa.Text),
)

requests = sa.Table('requests', metadata,
    sa.Column('id', sa.Integer(unsigned=True), primary_key=True, nullable=False),
    sa.Column('device_id', sa.Integer(unsigned=True),
        sa.ForeignKey('boards.id', ondelete='RESTRICT'),
        nullable=False),
    sa.Column('assignee', sa.String(256), nullable=False),
    sa.Column('status', sa.String(32), nullable=False),
    sa.Column('expires', sa.DateTime, nullable=False),
)                   

imaging_servers = sa.Table('imaging_servers', metadata,
    sa.Column('id', sa.Integer(unsigned=True), primary_key=True, nullable=False),
    sa.Column('fqdn', sa.String(256), nullable=False),
)

images = sa.Table('images', metadata,
    sa.Column('id', sa.Integer(unsigned=True), primary_key=True, nullable=False),
    sa.Column('name', sa.String(32), nullable=False),
    sa.Column('version', sa.Integer(unsigned=True), nullable=False),
    sa.Column('description', sa.Text, nullable=False),
    sa.Column('pxe_config_filename', sa.String(256), nullable=False),
)

logs = sa.Table('logs', metadata,
    sa.Column('board_id', sa.Integer(unsigned=True), nullable=False),
    sa.Column('ts', sa.DateTime, nullable=False),
    sa.Column('source', sa.String(32), nullable=False),
    sa.Column('message', sa.Text, nullable=False),
)