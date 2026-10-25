#!/usr/bin/env bash
# ==========================================
# Ziyo PostgreSQL Database Backup Script
# Creates compressed, timestamped pg_dump
# ==========================================

set -euo pipefail

BACKUP_DIR="/var/backups/ziyo"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/ziyo_db_${TIMESTAMP}.sql.gz"

mkdir -p "${BACKUP_DIR}"

echo "[$(date)] Initiating Ziyo PostgreSQL backup..."

# Reads credentials from standard PG environment variables (PGHOST, PGUSER, PGDATABASE, PGPASSWORD)
pg_dump -h "${PGHOST:-localhost}" -U "${PGUSER:-ziyo_app}" -d "${PGDATABASE:-ziyo_db}" -F c | gzip > "${BACKUP_FILE}"

echo "[$(date)] Backup completed successfully: ${BACKUP_FILE}"
ls -lh "${BACKUP_FILE}"

# Retain only last 14 days of backups
find "${BACKUP_DIR}" -name "ziyo_db_*.sql.gz" -type f -mtime +14 -delete
echo "[$(date)] Expired backups older than 14 days pruned."
