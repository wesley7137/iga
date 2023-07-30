import React, { useEffect, useRef, useState } from "react";
import * as d3 from "d3";
import { Close } from "@carbon/icons-react";

interface Node {
  id: number;
  x?: number;
  y?: number;
  fx?: number | null;
  fy?: number | null;
  index?: number;
  content?: string;
  title?: string;
}

interface Link {
  source: Node;
  target: Node;
}

interface KnowledgeGraphProps {
  graph?: {
    nodes: Node[];
    links: Link[];
  };
}

function KnowledgeGraph({ graph }: KnowledgeGraphProps) {
  const ref = useRef<SVGSVGElement | null>(null);
  const minimapRef = useRef<SVGSVGElement | null>(null);

  const [selectedNode, setSelectedNode] = useState<Node | null>(null);

  useEffect(() => {
    if (!graph || !ref.current) return;

    const nodes = graph?.nodes;
    const links = graph?.links;

    nodes.forEach((node, index) => {
      node.index = index;
    });

    // Calculate the degree of each node
    const degree = nodes.map(() => 0);
    links.forEach((link) => {
      degree[link.source.index!] += 1;
      degree[link.target.index!] += 1;
    });

    // Create a color scale based on degree
    const colorScale = d3
      .scaleSequential(d3.interpolateCool)
      .domain([0, d3.max(degree)]);

    const width = ref.current.clientWidth;
    const height = ref.current.clientHeight;

    const simulation = d3
      .forceSimulation(nodes)
      .force(
        "link",
        d3
          .forceLink(links)
          .id((d: Node) => d.id)
          .distance(50)
      )
      .force("charge", d3.forceManyBody())
      .force("center", d3.forceCenter(width / 2, height / 2));

    const svg = d3.select(ref.current).attr("viewBox", [0, 0, width, height]);

    const mainGraphContent = svg.append("g");

    // Add links
    // Add links
    const link = mainGraphContent
      .selectAll("line")
      .data(links)
      .enter()
      .append("line")
      .attr("stroke", "black") // Set stroke color
      .attr("stroke-width", 2); // Set stroke width

    // Add nodes
    const node = mainGraphContent
      .selectAll("circle")
      .data(nodes)
      .enter()
      .append("circle")
      .attr("r", 5)
      .style("fill", (d: Node, i: number) => colorScale(degree[i])) // Apply the color based on degree
      .attr("stroke-width", 3)
      .on("click", (event: MouseEvent, d: Node) => {
        node.each(function (p: Node) {
          d3.select(this)
            .classed("node-selected", p === d)
            .attr("r", p === d ? 8 : 5); // Increase the radius for the selected node, set back to regular radius for others
        });
        setSelectedNode(d);
      })
      .on("mouseover", (event: MouseEvent, d: Node) => {
        d3.select(event.currentTarget)
          .classed("node-hovered", true)
          .attr("r", 8); // Add the class to the hovered node
      })
      .on("mouseout", (event: MouseEvent, d: Node) => {
        d3.select(event.currentTarget)
          .classed("node-hovered", false)
          .attr("r", d === selectedNode ? 8 : 5); // Remove the class when hover ends
      });

    // Update graph on tick
    simulation.on("tick", () => {
      link
        .attr("x1", (d: Link) => d.source.x!)
        .attr("y1", (d: Link) => d.source.y!)
        .attr("x2", (d: Link) => d.target.x!)
        .attr("y2", (d: Link) => d.target.y!);

      node.attr("cx", (d: Node) => d.x!).attr("cy", (d: Node) => d.y!);
    });
  }, [graph]);

  return (
    <div className="w-full h-full grow relative overflow-hidden">
      <svg ref={ref} className="w-full h-full"></svg>
      {selectedNode && (
        <div className="absolute w-full bg-slate-50 p-6 flex flex-col gap-3 border rounded top-0 h-fit max-h-[30rem]">
          <h2 className="font-semibold">{selectedNode.title}</h2>
          <p className="text-sm">{selectedNode.content}</p>
          <button
            className="ml-auto absolute top-2 right-2 p-1 rounded hover:bg-slate-100"
            onClick={() => {
              setSelectedNode(null);
            }}
          >
            <Close />
          </button>
        </div>
      )}
    </div>
  );
}

export default KnowledgeGraph;
