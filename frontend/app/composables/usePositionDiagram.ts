import { useApi } from "./useApi";
import { useApiFetch } from "./useApiFetch";

type FilterOption = { label: string; value: string };

export type DiagramNodeDatum = {
  id: string;
  group: string;
  subGroup: string;
  label: string;
  shape?: string;
  icon?: string;
  nodeType?: "placed" | "no-connections" | "unassigned";
  locationId?: string | null;
  locationPath?: string[];
  locationPathIds?: string[];
};

export type DiagramLinkDatum = {
  source: string;
  target: string;
};

export type SiteConfig = {
  groupNodeId: string;
  panel: any;
};

export type DiagramData = {
  nodes: DiagramNodeDatum[];
  links: DiagramLinkDatum[];
  panels: any[];
};

export type DiagramOverview = {
  nodes: DiagramNodeDatum[];
  links: DiagramLinkDatum[];
  panels: any[];
  groupOrder: string[];
  maxLocationDepth: number;
};

export const usePositionDiagram = () => {
  const {
    getPositionDiagram,
    getDiagramLocations,
    getDiagramLocationPositions,
  } = useApi();
  const { baseURL } = useApiFetch();
  const backendOrigin = baseURL.replace(/\/?api\/?$/, "");

  const toAbsoluteImageUrl = (url?: string | null): string | null => {
    if (!url) return null;
    if (
      url.startsWith("http://") ||
      url.startsWith("https://") ||
      url.startsWith("data:")
    ) {
      return url;
    }
    if (url.startsWith("/uploads/")) {
      return `${backendOrigin}${url}`;
    }
    if (url.startsWith("/")) {
      return `${baseURL}${url}`;
    }
    return `${baseURL}/${url}`;
  };

  /** Lightweight initial call: nodes, links, and sites for hierarchical layout. */
  const loadOverview = async (): Promise<DiagramOverview> => {
    const response: any = await getDiagramLocations();

    const nodes: DiagramNodeDatum[] = (response.nodes || []).map((n: any) => ({
      id: n.id,
      group: n.group,
      subGroup: n.subGroup,
      label: n.label,
      shape: n.shape,
      icon: n.icon,
      nodeType: n.nodeType,
      locationId: n.locationId,
      locationPath: n.locationPath || [],
      locationPathIds: n.locationPathIds || [],
    }));

    const links: DiagramLinkDatum[] = (response.links || []).map((l: any) => ({
      source: l.source,
      target: l.target,
    }));

    const panels: any[] = response.panels || [];
    const groupOrder: string[] = response.groupOrder || [];
    const maxLocationDepth = response.maxLocationDepth || 1;

    return {
      nodes,
      links,
      panels,
      groupOrder,
      maxLocationDepth,
    };
  };

  /** On-demand call: full position node details for a single location. */
  const loadLocationData = async (
    locationId: string,
  ): Promise<DiagramNodeDatum[]> => {
    const response = await getDiagramLocationPositions(locationId);

    return (response.nodes || []).map((node: any) => ({
      id: node.id,
      group: node.group || null,
      subGroup: node.subGroup || null,
      label: node.label || node.id,
      shape: node.shape || "Square",
      icon: node.icon,
    }));
  };

  /** Legacy single-call loader (still used as fallback). */
  const loadDiagramData = async (filters: {
    location?: string;
    system?: string;
  }): Promise<DiagramData> => {
    const response: any = await getPositionDiagram(filters);

    const nodes: DiagramNodeDatum[] = (response.nodes || []).map(
      (node: any) => ({
        id: node.id,
        group: node.group || null,
        subGroup: node.subGroup || null,
        label: node.label || node.id,
        shape: node.shape || "Square",
        icon: node.icon,
      }),
    );

    const links: DiagramLinkDatum[] = (response.links || []).map((l: any) => ({
      source: l.source,
      target: l.target,
    }));

    return {
      nodes,
      links,
      panels: response.panels || [],
    };
  };

  return { loadOverview, loadLocationData, loadDiagramData };
};
