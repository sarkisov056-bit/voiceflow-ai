"""Abstract interface for AI skills.

This module defines the contract that a "skill" (a discrete capability or
tool that the AI assistant can invoke, e.g. checking a calendar or
looking up a product) must implement. No concrete skill is implemented in
this module — only the abstract interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Skill(ABC):
    """Abstract base class describing a single AI skill/tool.

    A ``Skill`` represents one discrete capability that can be exposed to
    the AI assistant and invoked as part of a conversation (for example,
    "look up order status" or "schedule a callback"). Concrete skills
    must inherit from this class and implement all abstract members.

    Depending on this abstraction (rather than a concrete skill class)
    allows ``SkillRegistry`` and other consumers to work with any number
    of interchangeable skills without being aware of their internal
    implementation (Open/Closed Principle, Liskov Substitution Principle).
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the unique, machine-readable name of this skill.

        Returns:
            The skill's unique name, used as its registry key.

        Raises:
            NotImplementedError: Always, since this is an unimplemented
                interface member. Concrete subclasses must override it.
        """
        raise NotImplementedError()

    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the skill's capability.

        Args:
            *args: Positional arguments defined by the concrete skill
                implementation.
            **kwargs: Keyword arguments defined by the concrete skill
                implementation.

        Returns:
            The result produced by executing the skill. The exact type
            will be defined once a concrete skill implementation is
            added.

        Raises:
            NotImplementedError: Always, since this is an unimplemented
                interface method. Concrete subclasses must override it.
        """
        raise NotImplementedError()
