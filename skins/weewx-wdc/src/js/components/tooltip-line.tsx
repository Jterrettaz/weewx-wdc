import React from "react";
import type { Point } from "@nivo/line";

interface TooltipPropsLine {
  point: Point;
  slice?: boolean;
}

export const TooltipLine: React.FC<TooltipPropsLine> = (
  props: TooltipPropsLine
): React.ReactElement => {
  return (
    <div
      style={{
        padding: "7px",
        color: "white",
        borderLeft: `5px solid ${props.point.serieColor}`,
        textAlign: "right",
      }}
      className="diagram-tooltip"
    >
      {!props.slice && (
        <div style={{ marginBottom: "5px" }}>{props.point.data.xFormatted}</div>
      )}
      <div>{props.point.data.yFormatted}</div>
    </div>
  );
};
