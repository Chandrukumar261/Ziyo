#!/usr/bin/env bash
# ==========================================
# Ziyo PostgreSQL Database Restoration Script
# Restores from a compressed pg_dump file
# ==========================================

set -euo pipefail

if [ -z "${1:-}" ]; then
    echo "Usage: $0 <path-to-backup-file.sql.gz>"
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "${BACKUP_FILE}" ]; then
    echo "Error: Backup file not found at ${BACKUP_FILE}"
    exit 1
fi

echo "WARNING: Restoring will overwrite existing tables in '${PGDATABASE:-ziyo_db}'."
read -p "Type 'RESTORE' to confirm: " CONFIRM

if [ "${CONFIRM}" != "RESTORE" ]; then
    echo "Restoration aborted."
    exit 0
fi

echo "[$(date)] Restoring database from ${BACKUP_FILE}..."
gunzip -c "${BACKUP_FILE}" | pg_restore -h "${PGHOST:-localhost}" -U "${PGUSER:-ziyo_app}" -d "${PGDATABASE:-ziyo_db}" --clean --if-exists

echo "[$(date)] Database restoration finished successfully."
