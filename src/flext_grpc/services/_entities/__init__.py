"""Private per-service entity classes for flext-grpc.

One class per module (ENFORCE-067). Hoisted out of the ``services/*`` facade
modules to break the deferred pydantic self-reference a nested manager class
creates when annotated on its own enclosing model (deferred-self-reference
check).
"""

from __future__ import annotations
