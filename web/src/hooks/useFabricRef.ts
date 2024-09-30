import { fabric } from "fabric";
import { useEffect } from "react";
import { FEATURE_COLORS, Region } from "../entities/Region";
import { o } from "ramda";

let config: any = {
    activeLine: undefined,
    activeShape: undefined,
    lineArray: [],
    pointArray: [],
    drawMode: false
}

fabric.Object.prototype.originX = 'center';
fabric.Object.prototype.originY = 'center';




export const useFabricRef = (canvas?: fabric.Canvas, feature?: string) => {

    console.log('useFabricRef', feature);

    function onMouseDown(this: any, options: any) {
        // debugger
        if(!canvas) return;
        if (config.drawMode) {
            if (options.target && options.target.id === config?.pointArray?.[0]?.id) {
                // when click on the first point
                generatePolygon(config.pointArray);
            } else {
                addPoint(options);
            }
        }

        const evt = options.e;
        if (evt.altKey === true) {
            this.isDragging = true;
            this.selection = false;
            this.lastPosX = evt.clientX;
            this.lastPosY = evt.clientY;
        }
    }

    function onMouseUp(this: any) {
        if(!canvas) return;
        this.isDragging = false;
        this.selection = true;
    }

    function onMouseMove(this: any, options: any) {
        if(!canvas) return;
    	if (this.isDragging) {
        	let e = options.e;
        	this.viewportTransform[4] += e.clientX - this.lastPosX;
            this.viewportTransform[5] += e.clientY - this.lastPosY;
            this.requestRenderAll();
            this.lastPosX = e.clientX;
            this.lastPosY = e.clientY;
        }
        if (config.drawMode) {
            if (config.activeLine && config.activeLine.class === 'line') {
                const pointer = canvas.getPointer(options.e);
                config.activeLine.set({
                    x2: pointer.x,
                    y2: pointer.y
                });
                const points = config.activeShape.get('points');
                points[config.pointArray.length] = {
                    x: pointer.x,
                    y: pointer.y,
                };
                config.activeShape.set({
                    points
                });
            }
            canvas.renderAll();
        }
    }

    function onMouseWheel(options: any) {
        if(!canvas) return;
        const delta = options.e.deltaY;
        const pointer = canvas.getPointer(options.e);
        let zoom = canvas.getZoom();
        if (delta > 0) {
            zoom += 0.02;
        } else {
            zoom -= 0.02;
        }
        if (zoom > 20) zoom = 20;
        if (zoom < 0.1) zoom = 0.1;
        canvas.zoomToPoint({ x: options.e.offsetX, y: options.e.offsetY }, zoom);
        options.e.preventDefault();
        options.e.stopPropagation();
      }

      function onObjectMove(option: any) {
        if(!canvas) return;
        const object = option.target;
        object._calcDimensions?.();
        object.setCoords();
        canvas.renderAll();
      }

      function toggleDrawPolygon(event: any) {
        if(!canvas) return;
        if (config.drawMode) {
            // stop draw mode
            config = {
                activeLine: null,
                activeShape: null,
                lineArray: [],
                pointArray: [],
                drawMode: false
            };
            canvas.selection = true;
        } else {
            // start draw mode
            canvas.selection = false;
            config.drawMode = true;
        }
    }

    function addPoint(options: any) {
        if(!canvas) return;
        const pointOption = {
            id: new Date().getTime(),
            radius: 5,
            fill: '#ffffff',
            stroke: '#333333',
            strokeWidth: 0.5,
            left: options.e.layerX / canvas.getZoom(),
            top: options.e.layerY / canvas.getZoom(),
            selectable: false,
            hasBorders: false,
            hasControls: false,
            originX: 'center',
            originY: 'center',
            objectCaching: false,
        };
        const point = new fabric.Circle(pointOption);

        if (config.pointArray.length === 0) {
            // fill first point with red color
            point.set({
                fill: 'red'
            });
        }

        const linePoints = [
            options.e.layerX / canvas.getZoom(),
            options.e.layerY / canvas.getZoom(),
            options.e.layerX / canvas.getZoom(),
            options.e.layerY / canvas.getZoom(),
        ];
        const lineOption = {
            strokeWidth: 2,
            fill: '#999999',
            stroke: '#999999',
            originX: 'center',
            originY: 'center',
            selectable: false,
            hasBorders: false,
            hasControls: false,
            evented: false,
            objectCaching: false,
        };
        const line = new fabric.Line(linePoints, lineOption);
        // @ts-ignore
        line.class = 'line';

        if (config.activeShape) {
            const pos = canvas.getPointer(options.e);
            const points = config.activeShape.get('points');
            points.push({
                x: pos.x,
                y: pos.y
            });
            const {polygon} = generatePolygonObject(String(new Date().getTime()), points);
            canvas.remove(config.activeShape);
            canvas.add(polygon);
            config.activeShape = polygon;
            canvas.renderAll();
        } else {
            const polyPoint = [{
                x: options.e.layerX / canvas.getZoom(),
                y: options.e.layerY / canvas.getZoom(),
            }, ];
            const {polygon} = generatePolygonObject(String(new Date().getTime()), polyPoint);
            config.activeShape = polygon;
            canvas.add(polygon);
        }

        config.pointArray.push(point);
        config.lineArray.push(line);
        config.activeLine = line;

        canvas.add(line);
        canvas.add(point);
    }

    function generatePolygon(pointArray: any) {
        if(!canvas) return;
        const points = [];
        // collect points and remove them from canvas
        for (const point of pointArray) {
            points.push({
                x: point.left,
                y: point.top,
            });
            canvas.remove(point);
        }

        // remove lines from canvas
        for (const line of config.lineArray) {
            canvas.remove(line);
        }

        // remove selected Shape and Line
        canvas.remove(config.activeShape).remove(config.activeLine);

        // create polygon from collected points
        const {polygon} = generatePolygonObject(String(new Date().getTime()), points, {
            // @ts-ignore
            id: new Date().getTime(),
            stroke: '#eee',
            fill: 'rgba(200,200,200,0.5)',
            objectCaching: false,
            moveable: false,
        })
        canvas.add(polygon);

        toggleDrawPolygon(undefined);
        editPolygon();
    }

    /**
     * define a function that can locate the controls.
     * this function will be used both for drawing and for interaction.
     */
	function polygonPositionHandler(this: any, dim: any, finalMatrix: any, fabricObject: any) {
        if(!canvas) return;
        const x = (fabricObject.points[this.pointIndex].x - fabricObject.pathOffset.x),
                y = (fabricObject.points[this.pointIndex].y - fabricObject.pathOffset.y);
            return fabric.util.transformPoint(
                { x: x, y: y } as fabric.Point,
        fabric.util.multiplyTransformMatrices(
            fabricObject.canvas.viewportTransform,
            fabricObject.calcTransformMatrix()
        )
            );
	}

    /**
     * define a function that will define what the control does
     * this function will be called on every mouse move after a control has been
     * clicked and is being dragged.
     * The function receive as argument the mouse event, the current trasnform object
     * and the current position in canvas coordinate
     * transform.target is a reference to the current object being transformed,
     */
    function actionHandler(eventData: any, transform: any, x: any, y: any) {
        if(!canvas) return;
        const polygon = transform.target,
            currentControl = polygon.controls[polygon.__corner],
            mouseLocalPosition = polygon.toLocalPoint(new fabric.Point(x, y), 'center', 'center'),
        polygonBaseSize = polygon._getNonTransformedDimensions(),
                size = polygon._getTransformedDimensions(0, 0),
                finalPointPosition = {
                    x: mouseLocalPosition.x * polygonBaseSize.x / size.x + polygon.pathOffset.x,
                    y: mouseLocalPosition.y * polygonBaseSize.y / size.y + polygon.pathOffset.y
                };
        polygon.points[currentControl.pointIndex] = finalPointPosition;
        return true;
    }

    /**
     * define a function that can keep the polygon in the same position when we change its
     * width/height/top/left.
     */
  function anchorWrapper(anchorIndex: any, fn: any) {
    if(!canvas) return;
    return function(eventData: any, transform: any, x: any, y: any) {
      const fabricObject = transform.target,
          absolutePoint = fabric.util.transformPoint({
              x: (fabricObject.points[anchorIndex].x - fabricObject.pathOffset.x),
              y: (fabricObject.points[anchorIndex].y - fabricObject.pathOffset.y),
          } as fabric.Point, fabricObject.calcTransformMatrix()),
          actionPerformed = fn(eventData, transform, x, y),
          newDim = fabricObject._setPositionDimensions({}),
          polygonBaseSize = fabricObject._getNonTransformedDimensions(),
          newX = (fabricObject.points[anchorIndex].x - fabricObject.pathOffset.x) / polygonBaseSize.x,
  		    newY = (fabricObject.points[anchorIndex].y - fabricObject.pathOffset.y) / polygonBaseSize.y;
      fabricObject.setPositionByOrigin(absolutePoint, newX + 0.5, newY + 0.5);
      return actionPerformed;
    }
  }

    function editPolygon() {
        if(!canvas) return;
        let activeObject = canvas.getActiveObject();
        if (!activeObject) {
            activeObject = canvas.getObjects().reverse()[0];
            canvas.setActiveObject(activeObject);
        }

        // @ts-ignore
        activeObject.edit = true;
        activeObject.objectCaching = false;

        // @ts-ignore
        const lastControl = activeObject.points.length - 1;
        activeObject.cornerStyle = 'circle';
        // @ts-ignore
        activeObject.controls = activeObject.points.reduce((acc: any, point: any, index: any) => {
            acc['p' + index] = new fabric.Control({
                // @ts-ignore
                positionHandler: polygonPositionHandler,
                actionHandler: anchorWrapper(index > 0 ? index - 1 : lastControl, actionHandler),
                actionName: 'modifyPolygon',
                pointIndex: index,
            });
            return acc;
        }, {});

        activeObject.hasBorders = false;

        canvas.requestRenderAll();
    }

    function resizePolygon() {
        if(!canvas) return;
        let activeObject = canvas.getActiveObject();
        if (!activeObject) {
            activeObject = canvas.getObjects().reverse()[0];
            canvas.setActiveObject(activeObject);
        }

        // @ts-ignore
        activeObject.edit = false;
        activeObject.objectCaching = false;
        activeObject.controls = fabric.Object.prototype.controls;
        activeObject.cornerStyle = 'rect';
        activeObject.hasBorders = true;

        canvas.requestRenderAll();
    }

    function generatePolygonObject(id: string, pointArray: any, options?: any) {
        const regionDraw = getPolygons().find(polygon => polygon.id === id);
        if(regionDraw) {
            return {polygon: regionDraw};
        }
        let fill = 'transparent';
        let stroke = 'rgba(202,54,1,1)';  // Cor da borda
        const featureToUse = options?.feature || feature;
        if(options && featureToUse && featureToUse in FEATURE_COLORS){
            options.fill = FEATURE_COLORS[featureToUse as keyof typeof FEATURE_COLORS];
            options.stroke = stroke;
        } else {
            options.fill = fill;
            options.stroke = stroke;
        }
        console.log(options);
        const polygon = new Region(id, `Region ${id}`, featureToUse || "---", pointArray, options ||{
            stroke: options.stroke,
            strokeWidth: 6,
            fill: options.fill,
            opacity: 1,
            selectable: false,
            hasBorders: false,
            hasControls: false,
            evented: false,
            objectCaching: false,
            ...options
        });


        return {polygon};
    }

    function getPolygons() {
        return canvas?.getObjects().filter(obj => obj instanceof Region) as Region[];
    }

    // function addPolygon(region: any) {
    //     if(!canvas) return;
    //     const pointsObj = region.polygon.map((point: any) => new fabric.Point(point[0], point[1]));
    //     const {polygon: polygonToAdd} = generatePolygonObject(region.id, pointsObj, {feature: region.feature_id, ...region});
    //     canvas.add(polygonToAdd);
    //     canvas.requestRenderAll();
    // }
    function addPolygon(region: any) {
        if (!canvas) return;
    
        // Check if region and its properties are defined
        if (!region || !region.polygon) {
            console.warn('Invalid region data:', region);
            return;
        }
    
        // Create points for the polygon
        const pointsObj: fabric.Point[] = region.polygon.map((point: number[]) => {
            if (Array.isArray(point) && point.length === 2) {
                return new fabric.Point(point[0], point[1]);
            } else {
                console.warn('Invalid point data:', point);
                return null;
            }
        }).filter((point: fabric.Point | null): point is fabric.Point => point !== null); // Filter out any null points
    
        if (pointsObj.length === 0) {
            console.warn('No valid points to add');
            return;
        }
    
        // Generate the polygon object
        const { polygon: polygonToAdd } = generatePolygonObject(region.id, pointsObj, { feature: region.feature_id, ...region });
    
        if (!polygonToAdd) {
            console.warn('Failed to generate polygon object');
            return;
        }
    
        // Add the polygon to the canvas
        canvas.add(polygonToAdd);
        canvas.requestRenderAll();
    }
    

    useEffect(() => {
        if(!canvas) return;
        canvas.on('mouse:down', onMouseDown);
        canvas.on('mouse:up', onMouseUp);
        canvas.on('mouse:move', onMouseMove);
        canvas.on('object:moving', onObjectMove);
        // canvas.on('mouse:wheel', onMouseWheel);

        return () => {
            canvas.off('mouse:down', onMouseDown);
            canvas.off('mouse:up', onMouseUp);
            canvas.off('mouse:move', onMouseMove);
            canvas.off('object:moving', onObjectMove);
            // canvas.off('mouse:wheel', onMouseWheel);
        }
    }, [canvas, feature]);

    return {draw: toggleDrawPolygon, canvas, active: canvas?.getActiveObject() as Region, resize: resizePolygon, edit: editPolygon, getPolygons, addPolygon};
};
