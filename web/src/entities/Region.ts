import { fabric } from "fabric";

const Polygon = fabric.Polygon;


export class Region extends Polygon {

    public id: string;
    public name: string;
    public feature: string;
    public percent_to_consider: number;

    constructor(id: string, name: string, feature: string, points: fabric.Point[], options?: any) {
        options = options || {};
        options.selectable = true;
        super(points, options);
        this.id = id;
        this.name = name;
        this.feature = feature;
        this.percent_to_consider = options?.percent_to_consider || 0;
    }
}

export const FEATURES = [
    { id: "slag_ladle", name: "roi_slag", color: "rgba(0, 141, 213, 0.6)" }
]

export const FEATURE_COLORS = FEATURES.reduce((acc, feature) => {
    acc[feature.id] = feature.color;
    return acc;
}, {} as any)
