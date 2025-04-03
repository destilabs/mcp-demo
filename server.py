from typing import Optional, List
from mcp.server.fastmcp import FastMCP
import datetime

from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tags: List[str] = []


# In-memory database
items_db: dict[int, Item] = {}
# Initialize FastMCP server
mcp = FastMCP("time-service")

@mcp.tool()
async def create_item_tool(name: str, price: float, description: Optional[str] = None, tags: List[str] = []) -> dict:
    """Create a new item in the database.

    Args:
        name (str): Name of the item to be created.
        price (float): Price of the item to be created.
        description (Optional[str]): Description of the item to be created.
        tags (List[str]): Tags for the item to be created.

    Returns:
        dict: The created item with its assigned ID.
    """
    new_id = len(items_db) + 1  # Generate a new ID
    new_item = Item(id=new_id, name=name, description=description, price=price, tags=tags)
    items_db[new_id] = new_item
    return new_item.model_dump()

# @mcp.tool()
# async def create_item_tool(item: Item) -> dict:
#     """Create a new item in the database.

#     Args:
#         name (str): Name of the item to be created.
#         price (float): Price of the item to be created.
#         description (Optional[str]): Description of the item to be created.
#         tags (List[str]): Tags for the item to be created.

#     Returns:
#         dict: The created item with its assigned ID.
#     """
#     new_id = len(items_db) + 1  # Generate a new ID
#     # new_item = Item(id=new_id, name=name, description=description, price=price, tags=tags)
#     items_db[new_id] = item
#     return items_db[new_id].model_dump()


@mcp.tool()
async def get_all_items_tool() -> List[dict]:
    """Retrieve all items from the database.

    Returns:
        List[dict]: A list of all items in the database.
    """
    return [item.model_dump() for item in items_db.values()]

@mcp.tool()
async def get_item_by_id_tool(item_id: int) -> Optional[dict]:
    """Retrieve an item from the database by its ID.

    Args:
        item_id (int): The ID of the item to retrieve.

    Returns:
        Optional[dict]: The item if found, otherwise None.
    """
    return items_db.get(item_id).model_dump() if item_id in items_db else None

@mcp.tool()
async def delete_item_by_id_tool(item_id: int) -> dict:
    """Delete an item from the database by its ID.

    Args:
        item_id (int): The ID of the item to delete.

    Returns:
        dict: A message indicating the result of the deletion.
    """
    if item_id in items_db:
        del items_db[item_id]
        return {"message": "Item deleted successfully."}
    return {"message": "Item not found."}

@mcp.tool()
async def read_item_by_id_tool(item_id: int) -> Optional[dict]:
    """Read an item from the database by its ID.

    Args:
        item_id (int): The ID of the item to read.

    Returns:
        Optional[dict]: The item if found, otherwise None.
    """
    return items_db.get(item_id).model_dump() if item_id in items_db else None

# Add sample data
sample_items = [
    Item(id=1, name="Hammer", description="A tool for hammering nails", price=9.99, tags=["tool", "hardware"]),
    Item(id=2, name="Screwdriver", description="A tool for driving screws", price=7.99, tags=["tool", "hardware"]),
    Item(id=3, name="Wrench", description="A tool for tightening bolts", price=12.99, tags=["tool", "hardware"]),
    Item(id=4, name="Saw", description="A tool for cutting wood", price=19.99, tags=["tool", "hardware", "cutting"]),
    Item(id=5, name="Drill", description="A tool for drilling holes", price=49.99, tags=["tool", "hardware", "power"]),
]

for item in sample_items:
    items_db[item.id] = item



if __name__ == "__main__":
    
    # Initialize and run the server
    mcp.run(transport="sse")
