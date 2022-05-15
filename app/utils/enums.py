from enum import Enum


class NetInsightEnum(str, Enum):
    def __str__(self):
        return self.__str__(self)


class Visibility(NetInsightEnum):
    open = "Open"
    restricted = "Restricted"


class SearchTypes(NetInsightEnum):
    approval = "Approval"
    audit = "Audit"
    inventory = "Inventory"
    ipadmin = "IPAdmin"
    debug = "Debug"
    network_config = "NetworkConfig"
    monitor = "Monitor"
    task = "Task"
    query = "Query"
    workspace = "Workspace"
    tool = "Tool"
    dcim = "DCIM"


class UserRoles(NetInsightEnum):
    superuser = "Superuser"
    manager = "Manager"
    admin = "Admin"
    member = "Member"
    enduser = "Enduser"


class QueryTimeRange(NetInsightEnum):
    hourly = "Hourly"
    daily = "Daily"
    weekly = "Weekly"
    monthly = "Monthly"
    yearly = "Yearly"
