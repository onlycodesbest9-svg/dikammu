from __future__ import annotations
import csv
import json
from pathlib import Path
from typing import List, Dict, Any
from hash_table import Record

class StorageManager:
    def __init__(self, autosave_path: Path | None = None) -> None:
        self.autosave_path = autosave_path or (Path.cwd() / "autosave_smarthash.json")

    def export_csv(self, file_path: Path, records: List[Record]) -> None:
        headers = ["mode", "id", "name", "price", "description", "hash_index", "inserted_at"]
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for r in records:
                writer.writerow({
                    "mode": r.mode,
                    "id": r.id,
                    "name": r.name,
                    "price": "" if r.price is None else r.price,
                    "description": "" if r.description is None else r.description,
                    "hash_index": r.hash_index if r.hash_index is not None else "",
                    "inserted_at": r.inserted_at if r.inserted_at is not None else ""
                })

    def import_csv(self, file_path: Path) -> List[Record]:
        out: List[Record] = []
        with open(file_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                mode = (row.get("mode") or "Item").strip()
                id_val = int(row.get("id") or 0)
                name = row.get("name") or ""
                price = row.get("price")
                description = row.get("description")
                price_val = float(price) if price not in (None, "",) else None
                desc_val = description if description not in (None,) else None
                out.append(Record(
                    mode=mode,
                    id=id_val,
                    name=name,
                    price=price_val,
                    description=desc_val
                ))
        return out

    def autosave_json(self, records: List[Record]) -> None:
        data: List[Dict[str, Any]] = []
        for r in records:
            data.append({
                "mode": r.mode,
                "id": r.id,
                "name": r.name,
                "price": r.price,
                "description": r.description,
            })
        with open(self.autosave_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_autosave(self) -> List[Record]:
        if not self.autosave_path.exists():
            return []
        with open(self.autosave_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        out: List[Record] = []
        for row in raw:
            out.append(Record(
                mode=row.get("mode", "Item"),
                id=int(row.get("id", 0)),
                name=row.get("name", ""),
                price=row.get("price"),
                description=row.get("description"),
            ))
        return out
