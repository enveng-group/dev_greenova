#!/usr/bin/env python3
"""Convert BPMN workflow to swim lane diagram using Graphviz.

This script parses the Greenova BPMN workflow file and generates
a swim lane diagram in SVG or PDF format using Graphviz DOT notation.
SVG format provides better screen readability with scalable text and graphics.

Author: Adrian Gallo
License: AGPL-3.0
"""

import argparse
import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Literal

import graphviz
from beartype import beartype

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class BPMNParser:
    """Parse BPMN XML and extract workflow elements."""

    def __init__(self) -> None:
        """Initialize the BPMN parser."""
        self.namespaces = {
            "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        }
        self.lanes: dict[str, str] = {}
        self.nodes: dict[str, dict[str, str]] = {}
        self.flows: list[dict[str, str]] = []
        self.subprocesses: dict[str, list[str]] = {}

    @beartype
    def parse_bpmn_file(self, file_path: Path) -> None:
        """Parse BPMN XML file and extract workflow elements.

        Args:
            file_path: Path to the BPMN XML file.

        Raises:
            FileNotFoundError: If BPMN file does not exist.
            ET.ParseError: If XML parsing fails.

        """
        if not file_path.exists():
            msg = f"BPMN file not found: {file_path}"
            raise FileNotFoundError(msg)

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Extract lanes
            self._extract_lanes(root)

            # Extract process elements
            self._extract_process_elements(root)

            logger.info("Successfully parsed BPMN file")
            logger.info(
                "Found %d lanes, %d nodes, %d flows",
                len(self.lanes),
                len(self.nodes),
                len(self.flows),
            )

        except ET.ParseError as e:
            logger.exception("Failed to parse BPMN XML: %s", e)
            raise

    @beartype
    def _extract_lanes(self, root: ET.Element) -> None:
        """Extract lane information from BPMN."""
        lane_elements = root.findall(".//bpmn:lane", self.namespaces)
        for lane in lane_elements:
            lane_id = lane.get("id", "")
            lane_name = lane.get("name", "")
            if lane_id and lane_name:
                self.lanes[lane_id] = lane_name
                logger.debug("Found lane: %s -> %s", lane_id, lane_name)

    @beartype
    def _extract_process_elements(self, root: ET.Element) -> None:
        """Extract all process elements (nodes and flows)."""
        process = root.find(".//bpmn:process", self.namespaces)
        if process is None:
            logger.warning("No process element found in BPMN")
            return

        # Extract various node types
        self._extract_events(process)
        self._extract_tasks(process)
        self._extract_gateways(process)
        self._extract_subprocesses(process)

        # Extract sequence flows
        self._extract_sequence_flows(process)

    @beartype
    def _extract_events(self, process: ET.Element) -> None:
        """Extract start and end events."""
        # Start events
        start_events = process.findall(".//bpmn:startEvent", self.namespaces)
        for event in start_events:
            self._add_node(event, "startEvent")

        # End events
        end_events = process.findall(".//bpmn:endEvent", self.namespaces)
        for event in end_events:
            self._add_node(event, "endEvent")

    @beartype
    def _extract_tasks(self, process: ET.Element) -> None:
        """Extract user tasks and service tasks."""
        # User tasks
        user_tasks = process.findall(".//bpmn:userTask", self.namespaces)
        for task in user_tasks:
            self._add_node(task, "userTask")

        # Service tasks
        service_tasks = process.findall(".//bpmn:serviceTask", self.namespaces)
        for task in service_tasks:
            self._add_node(task, "serviceTask")

    @beartype
    def _extract_gateways(self, process: ET.Element) -> None:
        """Extract exclusive gateways."""
        gateways = process.findall(".//bpmn:exclusiveGateway", self.namespaces)
        for gateway in gateways:
            self._add_node(gateway, "exclusiveGateway")

    @beartype
    def _extract_subprocesses(self, process: ET.Element) -> None:
        """Extract subprocess elements."""
        subprocesses = process.findall(".//bpmn:subProcess", self.namespaces)
        for subprocess in subprocesses:
            subprocess_id = subprocess.get("id", "")
            subprocess_name = subprocess.get("name", "")

            if subprocess_id:
                self.nodes[subprocess_id] = {
                    "id": subprocess_id,
                    "name": subprocess_name,
                    "type": "subProcess",
                }

                # Extract internal elements of subprocess
                internal_elements = [
                    child.get("id") for child in subprocess if child.get("id")
                ]

                self.subprocesses[subprocess_id] = internal_elements

    @beartype
    def _extract_sequence_flows(self, process: ET.Element) -> None:
        """Extract sequence flows between elements."""
        flows = process.findall(".//bpmn:sequenceFlow", self.namespaces)
        for flow in flows:
            flow_id = flow.get("id", "")
            source_ref = flow.get("sourceRef", "")
            target_ref = flow.get("targetRef", "")
            flow_name = flow.get("name", "")

            if flow_id and source_ref and target_ref:
                self.flows.append(
                    {
                        "id": flow_id,
                        "source": source_ref,
                        "target": target_ref,
                        "name": flow_name,
                    }
                )

    @beartype
    def _add_node(self, element: ET.Element, node_type: str) -> None:
        """Add a node to the nodes dictionary."""
        node_id = element.get("id", "")
        node_name = element.get("name", "")

        if node_id:
            self.nodes[node_id] = {
                "id": node_id,
                "name": node_name,
                "type": node_type,
            }


class SwimLaneDiagramGenerator:
    """Generate swim lane diagram using Graphviz."""

    def __init__(
        self, parser: BPMNParser, output_format: Literal["pdf", "svg"] = "pdf"
    ) -> None:
        """Initialize the swim lane diagram generator.

        Args:
            parser: BPMN parser containing workflow data.
            output_format: Output format ('pdf' or 'svg').

        """
        self.parser = parser
        self.output_format = output_format
        self.dot = graphviz.Digraph(
            name="greenova_swimlane",
            comment="Greenova Environmental Management System Workflow",
            format=output_format,
        )

        # Configure diagram attributes for better readability
        self.dot.attr(rankdir="TB", size="16,20", ratio="fill")
        self.dot.attr("node", fontname="Arial", fontsize="14", fontweight="bold")
        self.dot.attr("edge", fontname="Arial", fontsize="12")

    @beartype
    def generate_diagram(self, output_path: Path) -> None:
        """Generate the swim lane diagram.

        Args:
            output_path: Path where to save the PDF diagram.

        """
        logger.info("Generating swim lane diagram...")

        # Create swim lanes as subgraphs
        self._create_swim_lanes()

        # Add nodes to appropriate lanes
        self._add_nodes_to_lanes()

        # Add edges/flows
        self._add_flows()

        # Render the diagram
        self._render_diagram(output_path)

    @beartype
    def _create_swim_lanes(self) -> None:
        """Create swim lanes as subgraphs."""
        for lane_id, lane_name in self.parser.lanes.items():
            with self.dot.subgraph(name=f"cluster_{lane_id}") as lane_graph:
                lane_graph.attr(
                    label=lane_name,
                    style="filled",
                    fillcolor="lightblue",
                    fontsize="16",
                    fontweight="bold",
                )
                lane_graph.attr("node", style="filled", fillcolor="white")

    @beartype
    def _add_nodes_to_lanes(self) -> None:
        """Add workflow nodes to appropriate swim lanes."""
        # Create lane assignments based on node types
        lane_assignments = self._assign_nodes_to_lanes()

        for lane_id, lane_name in self.parser.lanes.items():
            with self.dot.subgraph(name=f"cluster_{lane_id}") as lane_graph:
                lane_graph.attr(
                    label=lane_name,
                    style="filled",
                    fillcolor="lightblue",
                    fontsize="12",
                    fontweight="bold",
                )

                # Add nodes assigned to this lane
                for node_id in lane_assignments.get(lane_id, []):
                    node = self.parser.nodes.get(node_id)
                    if node:
                        self._add_node_to_lane(lane_graph, node)

    @beartype
    def _assign_nodes_to_lanes(self) -> dict[str, list[str]]:
        """Assign nodes to swim lanes based on their type and context.

        Returns:
            Dictionary mapping lane IDs to lists of node IDs.

        """
        lane_assignments: dict[str, list[str]] = {
            lane_id: [] for lane_id in self.parser.lanes
        }

        # Assign nodes based on type
        for node_id, node in self.parser.nodes.items():
            node_type = node.get("type", "")

            # User-facing tasks go to user lane
            if node_type in {"userTask", "startEvent", "endEvent"}:
                if "lane_user" in lane_assignments:
                    lane_assignments["lane_user"].append(node_id)

            # System tasks go to system lane
            elif node_type in {"serviceTask", "subProcess"}:
                if "lane_system" in lane_assignments:
                    lane_assignments["lane_system"].append(node_id)

            # Gateways can go to either lane based on context
            elif node_type == "exclusiveGateway":
                # Assign to user lane by default
                if "lane_user" in lane_assignments:
                    lane_assignments["lane_user"].append(node_id)

        return lane_assignments

    @beartype
    def _add_node_to_lane(
        self,
        lane_graph: graphviz.Digraph,
        node: dict[str, str],
    ) -> None:
        """Add a single node to a swim lane."""
        node_id = node["id"]
        node_name = node.get("name", node_id)
        node_type = node.get("type", "")

        # Define node shapes and colors based on type
        shape, color = self._get_node_style(node_type)

        # Truncate long names for better display
        display_name = self._truncate_name(node_name)

        lane_graph.node(
            node_id,
            label=display_name,
            shape=shape,
            fillcolor=color,
            style="filled",
        )

    @beartype
    def _get_node_style(self, node_type: str) -> tuple[str, str]:
        """Get node shape and color based on type.

        Args:
            node_type: Type of the BPMN node.

        Returns:
            Tuple of (shape, color) for the node.

        """
        style_map = {
            "startEvent": ("circle", "lightgreen"),
            "endEvent": ("doublecircle", "lightcoral"),
            "userTask": ("box", "lightblue"),
            "serviceTask": ("box", "lightyellow"),
            "exclusiveGateway": ("diamond", "orange"),
            "subProcess": ("box3d", "lightgray"),
        }

        return style_map.get(node_type, ("box", "white"))

    @beartype
    def _truncate_name(self, name: str, max_length: int = 30) -> str:
        """Truncate node names for better display.

        Args:
            name: Original name.
            max_length: Maximum length for display.

        Returns:
            Truncated name with ellipsis if needed.

        """
        if len(name) <= max_length:
            return name
        return name[: max_length - 3] + "..."

    @beartype
    def _add_flows(self) -> None:
        """Add sequence flows as edges between nodes."""
        for flow in self.parser.flows:
            source = flow["source"]
            target = flow["target"]
            flow_name = flow.get("name", "")

            # Only add edge if both source and target nodes exist
            if source in self.parser.nodes and target in self.parser.nodes:
                edge_label = self._truncate_name(flow_name, 20) if flow_name else ""
                self.dot.edge(source, target, label=edge_label)

    @beartype
    def _render_diagram(self, output_path: Path) -> None:
        """Render the diagram to the specified format.

        Args:
            output_path: Path where to save the diagram.

        """
        try:
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Remove extension if present (graphviz adds it)
            output_name = str(output_path)
            if output_name.endswith(f".{self.output_format}"):
                output_name = output_name[: -len(self.output_format) - 1]

            # Render the diagram
            self.dot.render(output_name, cleanup=True)

            logger.info(
                "Swim lane diagram saved to: %s.%s", output_name, self.output_format
            )

        except Exception as e:
            logger.exception("Failed to render diagram: %s", e)
            raise


@beartype
def main() -> None:
    """Main function to convert BPMN to swim lane diagram."""
    parser = argparse.ArgumentParser(
        description="Convert BPMN workflow to swim lane diagram",
    )
    parser.add_argument(
        "--format",
        choices=["svg", "pdf"],
        default="svg",
        help="Output format (default: svg for better screen readability)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file path (extension will be added automatically)",
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Input BPMN file path",
    )

    args = parser.parse_args()

    # Define file paths
    project_root = Path(__file__).parent.parent
    bpmn_file = args.input or (project_root / "Greenova-Workflow-Clean.bpmn")

    # Determine output file with proper extension
    if args.output:
        output_file = args.output
    else:
        output_file = project_root / "docs" / f"greenova_swimlane_diagram.{args.format}"

    try:
        # Parse BPMN file
        bpmn_parser = BPMNParser()
        bpmn_parser.parse_bpmn_file(bpmn_file)

        # Generate swim lane diagram
        generator = SwimLaneDiagramGenerator(bpmn_parser, args.format)
        generator.generate_diagram(output_file)

        logger.info("Successfully converted BPMN to swim lane diagram")
        logger.info("Output format: %s", args.format.upper())
        logger.info(
            "SVG files provide better screen readability and can be zoomed without quality loss"
        )

    except Exception as e:
        logger.exception("Failed to convert BPMN to swim lane diagram: %s", e)
        raise


if __name__ == "__main__":
    main()
