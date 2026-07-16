"""Skill registry shell for future skill discovery and lookup."""

from collections.abc import Sequence

from app.ai.skills.interfaces import Skill


class SkillRegistry:
    """Coordinates future registration and lookup of AI skills.

    The registry is intended to provide a small, explicit boundary between
    conversation orchestration and concrete skill implementations. Future code can
    use this class to register, list, and retrieve capabilities while keeping
    orchestration logic independent from individual skill classes.

    The current class does not maintain internal state or global registries.
    Future implementations should avoid singleton patterns and receive any
    required storage or configuration through dependency injection.
    """

    def register(self, name: str, skill: Skill) -> None:
        """Register a skill under a stable name.

        Args:
            name: Unique skill name used for later lookup.
            skill: Skill implementation associated with the name.
        """
        raise NotImplementedError()

    def get(self, name: str) -> Skill:
        """Return a registered skill by name.

        Args:
            name: Unique skill name to resolve.

        Returns:
            Skill implementation associated with the provided name.
        """
        raise NotImplementedError()

    def list(self) -> Sequence[str]:
        """List registered skill names.

        Returns:
            Ordered collection of registered skill names.
        """
        raise NotImplementedError()
