"""Skill registry.

This module defines ``SkillRegistry``, the future entry point for
registering ``Skill`` implementations and looking them up by name so the
AI assistant can discover and invoke them. At this stage the class only
defines its intended public API; no business logic has been implemented
yet.
"""

from __future__ import annotations

from app.ai.skills.interfaces import Skill


class SkillRegistry:
    """Registers and provides lookup for available AI skills.

    ``SkillRegistry`` is intended to hold the set of :class:`Skill`
    instances available to the AI assistant for a given context (e.g. a
    conversation or an application instance), and to provide lookup of a
    skill by name so it can be invoked.

    Each ``SkillRegistry`` instance owns its own set of registered
    skills; the registry is explicitly constructed and passed to whatever
    component needs it, rather than being implemented as a singleton or
    exposed through global state. This keeps skill availability scoped
    and testable, and keeps ``SkillRegistry`` depending only on the
    ``Skill`` abstraction, not on any concrete skill (Dependency
    Inversion Principle).

    No business logic is implemented yet. Every public method currently
    raises ``NotImplementedError`` and will be filled in during a later
    iteration.
    """

    def register(self, skill: Skill) -> None:
        """Register a skill with this registry.

        Args:
            skill: The skill instance to register.

        Raises:
            NotImplementedError: Always, at this stage of development.
        """
        raise NotImplementedError()

    def get(self, name: str) -> Skill:
        """Look up a registered skill by its unique name.

        Args:
            name: The unique name of the skill to look up.

        Returns:
            The matching ``Skill`` instance.

        Raises:
            NotImplementedError: Always, at this stage of development.
        """
        raise NotImplementedError()

    def list_skills(self) -> list[Skill]:
        """List all skills currently registered with this registry.

        Returns:
            A list of all registered ``Skill`` instances.

        Raises:
            NotImplementedError: Always, at this stage of development.
        """
        raise NotImplementedError()
