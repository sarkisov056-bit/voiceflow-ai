"""Interfaces for future AI skill implementations."""

from abc import ABC, abstractmethod
from typing import Any


class Skill(ABC):
    """Abstract contract for a callable AI skill.

    Skills represent optional capabilities that future conversation workflows may
    discover and execute without knowing concrete implementation details. This
    abstraction keeps skill execution separate from registration and orchestration
    so each implementation can focus on one capability.

    The interface intentionally avoids prescribing transport, persistence, or
    provider behavior. Concrete skills should define their own dependencies
    through constructor injection when implemented.
    """

    @abstractmethod
    async def execute(self, **kwargs: Any) -> Any:
        """Execute the skill with keyword arguments supplied by the caller.

        Args:
            **kwargs: Skill-specific execution parameters.

        Returns:
            Skill-specific execution result.
        """
        raise NotImplementedError()
