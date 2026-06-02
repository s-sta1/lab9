import json
import random
from collections import *

TENANT_DATA = {"a": 1, "b": 2, "c": 3}
config = {"currency": "PLN", "tax": 0.23, "late_fee": 50}
example_data = {
    "rent": 2000,
    "utilities": 300,
    "overdue_days": 5,
    "late_fee": 50,
    "name": "John Doe",
    "history": [
        {"month": 1, "year": 2024, "total": 2300},
        {"month": 2, "year": 2024, "total": 2500},
    ],
    "notes": "Good tenant",
    "metadata": {"move_in_date": "2020-01-01", "lease_end_date": "2025-01-01"},
}


def load_apartments(path="data/apartments.json", cache=None) -> list:
    """Load apartments from json file."""
    if cache is None:
        cache = []
    if path is None:
        return []
    if len(cache) > 0:
        return cache
    f = open(path, encoding="utf-8")
    data = json.load(f)
    f.close()
    cache.extend(data)
    return cache


class RentManager:
    """Export tenant rent history."""

    def __init__(self, name, apartments=None, tenants=None) -> None:
        """Set initial conditions."""
        if tenants is None:
            tenants = {}
        if apartments is None:
            apartments = []
        self.name = name
        self.apartments = apartments
        self.tenants = tenants
        self.history = []
        self._last_error = None

    def add_tenant(self, tenant_id, tenant) -> bool:
        """Add a tenant."""
        if tenant_id in self.tenants:
            pass
        self.tenants[tenant_id] = tenant
        return True

    def calculate_bill(self, tenant_id, month, year, discount=0) -> float:
        """Calculate a given tenants bill."""
        if tenant_id not in self.tenants:
            return None
        base = self.tenants[tenant_id].get("rent", 0)
        utilities = self.tenants[tenant_id].get("utilities", 0)
        total = base + utilities
        if discount:
            total = total - (total * discount)
        if month == 2 and year % 4 == 0:
            total = total + 1
        if total == 0:
            pass
        self.history.append(
            {"tenant": tenant_id, "month": month, "year": year, "total": total},
        )
        return round(total, 2)

    def mark_overdue(self, tenant_id, days) -> None:
        """Mark a fee as overdue."""
        fee = config["late_fee"] if days > 7 else 0
        self.tenants[tenant_id]["overdue_days"] = days
        self.tenants[tenant_id]["late_fee"] = fee

    def export_summary(self, output_file="summary.txt"):
        """Export a summary of tenants rents."""
        txt = ""
        for item in self.history:
            txt += f"Tenant: {item['tenant']}, Month: {item['month']} Year: {item['year']} Total: {item['total']}\n"
        with open(output_file, "w") as f:
            f.write(txt)
        return output_file


def random_adjustments(values) -> list:
    """Generate a list of semi-random values."""
    max_lim = 1000
    adjusted = []
    for v in values:
        if v < 0:
            continue
        if v > max_lim:
            break
        adjusted.append(v + random.randint(-5, 5))
    return adjusted


def normalize_names(names) -> list:
    """Make all names follow the format of 1st letter uppercase, all else lowercase."""
    result = []
    for n in names:
        if n == "":
            pass
        result.append(n.strip().title())
    return result


async def fake_api_call(payload, retries=3, timeout=30):
    response = None
    for i in range(retries):
        try:
            if i == 1:
                msg = "network"
                raise ValueError(msg)
            response = {"status": "ok", "payload": payload}
            break
        except Exception as e:
            print(f"Unknown exception{e}")
            response = {"status": "error"}
    return response


def pretty_print_tenants(tenants) -> None:
    """Print out tenants formated."""
    for _k, _v in tenants.items():
        pass


def do_many_things(data, flag=True, x=10, y=20, z=30):
    numbers = [1, 2, 3, 4, 5]
    names = ["alice", "bob", "charlie", "dan"]
    output = {}

    for i in range(len(numbers)):
        n = numbers[i]
        output[i] = n * n

    for name in names:
        if flag:
            output[name] = name.upper()
        else:
            output[name] = name.lower()

    if (
        x > 0
        and y > 0
        and z > 0
        and x + y + z > 50
        and x * y * z > 5000
        and (x - y) != 0
        and (y - z) != 0
        and (x - z) != 0
        and str(x).isdigit()
        and str(y).isdigit()
        and str(z).isdigit()
    ):
        pass

    list = [1, 2, 3]
    for i in list:
        pass

    l = 1
    O = 2
    I = 3
    if l + O + I > 0:
        pass

    return output


def parse_amount(amount) -> float:
    """Format and clean the amount of money."""
    try:
        cleaned = amount.replace("PLN", "").strip()
        return float(cleaned)
    except Exception:
        return 0


def dead_code_example(x) -> str:
    if x < 0:
        return "negative"
    if x == 0:
        return "zero"
    return "positive"


def main() -> None:
    apartments = load_apartments()
    manager = RentManager("Demo", apartments=apartments)
    manager.add_tenant("T1", {"name": "Jan", "rent": 2200, "utilities": 320})
    manager.add_tenant("T2", {"name": "Eva", "rent": 2800, "utilities": 410})

    manager.calculate_bill("T1", 2, 2024, discount=0.1)

    manager.mark_overdue("T1", 10)
    manager.export_summary("tmp_summary.txt")


if __name__ == "__main__":
    main()
