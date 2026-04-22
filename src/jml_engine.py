import csv, json, logging, sys
from pathlib import Path
from auth import get_graph_token
from joiner import handle_joiner
from mover import handle_mover
from leaver import handle_leaver

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_PATH = BASE_DIR / "logs" / "actions.log"
(BASE_DIR / "logs").mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(LOG_PATH)]
)
logger = logging.getLogger(__name__)

def run():
    token = get_graph_token()
    with open(BASE_DIR / "data" / "dept_groups.json") as f:
        dept_group_map = json.load(f)
    with open(BASE_DIR / "data" / "employees.csv", newline="") as f:
        employees = list(csv.DictReader(f))

    for row in employees:
        status = row.get("status", "").strip().lower()
        try:
            if status == "new":
                handle_joiner(token, row, dept_group_map)
            elif status == "moved":
                handle_mover(token, row, dept_group_map)
            elif status == "left":
                handle_leaver(token, row)
            else:
                logger.warning(f"Unknown status: {status}")
        except Exception as e:
            logger.error(f"Error processing {row.get('upn')}: {e}")

if __name__ == "__main__":
    run()
