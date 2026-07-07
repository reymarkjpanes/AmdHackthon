import { describe, it, expect, afterEach } from "vitest";
import { render, cleanup, screen } from "@testing-library/react";
import fc from "fast-check";
import { RiskBadge, EvidenceBox } from "../Badges";

afterEach(() => {
  cleanup();
});

const ALL_COLORS = ["var(--amd-signal)", "var(--caution)", "var(--cleared)"];

function expectedColorFor(level: "HIGH" | "MEDIUM" | "LOW"): string {
  if (level === "HIGH") return "var(--amd-signal)";
  if (level === "MEDIUM") return "var(--caution)";
  return "var(--cleared)";
}

describe("RiskBadge property tests", () => {
  // Feature: clausify-ui-redesign, Property 6: RiskBadge color is determined exclusively by risk level
  it("uses the color mapped to the risk level and no other color, for any level", () => {
    fc.assert(
      fc.property(fc.constantFrom("HIGH", "MEDIUM", "LOW"), (level) => {
        cleanup();
        render(<RiskBadge variant={level} />);
        const badge = screen.getByText(level);
        const expected = expectedColorFor(level);

        expect(badge.style.color).toBe(expected);

        // Assert none of the other level colors are used.
        for (const color of ALL_COLORS) {
          if (color !== expected) {
            expect(badge.style.color).not.toBe(color);
          }
        }
      }),
      { numRuns: 100 },
    );
  });
});

describe("EvidenceBox", () => {
  // Feature: clausify-ui-redesign, Property 7: EvidenceBoxes in AI messages use parchment background with dark text
  it("uses parchment background with dark text by default (Property 7)", () => {
    fc.assert(
      fc.property(
        fc.string().filter((s) => s.trim().length > 0),
        (quote) => {
          const { container, unmount } = render(<EvidenceBox quote={quote} />);
          const el = container.firstElementChild as HTMLElement;
          if (el.style.background !== "var(--parchment)") return false;
          if (el.style.color !== "var(--lead)") return false;
          unmount();
          return true;
        },
      ),
      { numRuns: 100 },
    );
  });

  // Feature: clausify-ui-redesign, Property 5: EvidenceBoxes inside ConflictAlert use paper background with dark text
  it("respects a style override of paper background with dark text (Property 5)", () => {
    fc.assert(
      fc.property(
        fc.string().filter((s) => s.trim().length > 0),
        (quote) => {
          const { container, unmount } = render(
            <EvidenceBox
              quote={quote}
              style={{ background: "var(--paper)", color: "var(--ink)" }}
            />,
          );
          const el = container.firstElementChild as HTMLElement;
          if (el.style.background !== "var(--paper)") return false;
          if (el.style.color !== "var(--ink)") return false;
          unmount();
          return true;
        },
      ),
      { numRuns: 100 },
    );
  });
});
