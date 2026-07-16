"""System prompt shell for future AI Core prompt composition."""


class SystemPrompt:
    """Represents future construction of the default AI system prompt.

    This class is reserved for prompt composition concerns and intentionally does
    not define a hard-coded prompt or global constant. Encapsulating prompt
    construction in a class leaves room for future dependency injection,
    localization, configuration, and testing without spreading prompt-building
    logic across the codebase.
    """

    def build(self) -> str:
        """Build the system prompt text.

        Returns:
            System prompt text to be supplied to future AI provider calls.
        """
        raise NotImplementedError()
