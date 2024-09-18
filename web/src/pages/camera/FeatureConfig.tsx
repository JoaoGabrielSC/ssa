import React, { useEffect, useState } from 'react';
import { FabricJSCanvas, useFabricJSEditor } from 'fabricjs-react';
import { fabric } from 'fabric';
import styles from "./FeatureConfig.module.scss";
import { Button, Col, Row, notification } from 'antd';
import { useFabricRef } from '../../hooks/useFabricRef';

export const FeatureConfig = ({ params }: any) => {
    const { editor, onReady } = useFabricJSEditor();
    const [feature, setFeature] = useState<string | undefined>('KR_ROI');
    const [regionsToAdd, setRegionsToAdd] = useState<any[]>([]);
    const { draw: addRegion, canvas, active, edit, resize, addPolygon } = useFabricRef(editor?.canvas, feature);

    useEffect(() => {
        if (!canvas) return;
    
        const canvasWidth = 1080;
        const canvasHeight = 720;

        const updateBackgroundImage = () => {
            fabric.Image.fromURL(`http://localhost:5050/background_kr/`, function (oImg) {
                oImg.set({
                    top: 0,
                    left: 0,
                    originX: 'left',
                    originY: 'top',
                    selectable: false,
                    hasControls: false,
                    hasBorders: false,
                    lockMovementX: true,
                    lockMovementY: true,
                    lockScalingX: true,
                    lockScalingY: true,
                    lockRotation: true,
                    hoverCursor: 'default',
                    evented: false
                });

                canvas.setWidth(canvasWidth);
                canvas.setHeight(canvasHeight);

                oImg.scaleToWidth(canvasWidth);
                oImg.scaleToHeight(canvasHeight);

                canvas.setBackgroundImage(oImg, canvas.renderAll.bind(canvas));
                canvas.add(oImg);

                // Ajustar a posição e tamanho das regiões, se necessário
                if (regionsToAdd.length > 0) {
                    const region = regionsToAdd[0];
                    if (region && Array.isArray(region.polygon)) {
                        addPolygon(region);  // Adiciona a região ao canvas
                    } else {
                        console.warn('Polygon inválido ou indefinido:', region);
                    }
                }
            });
        };

        updateBackgroundImage();
    }, [canvas, regionsToAdd]);

    useEffect(() => {
        if (!canvas) return;

        const onDoubleClick = (event: any) => {
            const pointer = canvas.getPointer(event.e); // Get click position
            const clickedObject = canvas.findTarget(event.e, false);

            if (clickedObject && clickedObject.type === 'polygon') {
                const polygon = clickedObject as fabric.Polygon;
                const points = polygon.get("points") as fabric.Point[];
                const newPoint = { x: pointer.x, y: pointer.y };

                let closestIndex = 0;
                let minDistance = Infinity;

                for (let i = 0; i < points.length; i++) {
                    const nextIndex = (i + 1) % points.length;
                    const distance = distanceFromPointToLine(
                        points[i],
                        points[nextIndex],
                        newPoint
                    );

                    if (distance < minDistance) {
                        minDistance = distance;
                        closestIndex = nextIndex;
                    }
                }

                points.splice(closestIndex, 0, new fabric.Point(newPoint.x, newPoint.y));
                polygon.set({ points });
                canvas.renderAll();
            }
        };

        canvas.on('mouse:dblclick', onDoubleClick);

        return () => {
            canvas.off('mouse:dblclick', onDoubleClick);
        };
    }, [canvas]);

    // Função para buscar regiões do banco de dados
    const fetchRegions = () => {
        fetch("http://localhost:5050/get_regions")
            .then(response => response.json())
            .then(data => {
                console.log('Fetched regions:', data);
                // Atualiza o estado com a região recebida
                setRegionsToAdd([data]);  // Ajuste: Envolve a resposta em um array
            });
    }

    useEffect(() => {
        fetchRegions();  // Buscar as regiões do banco de dados ao carregar a página
    }, []);

    const onRemove = () => {
        if (!active) return;

        canvas?.remove(active);
        canvas?.renderAll();

        fetch('http://localhost:5050/remove_region', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: active?.id }),
        })
    }

    const onSubmit = () => {
        const values = {
            "feature_id": active?.feature || feature,
            "polygon": active?.points?.map((point: any) => ([point.x, point.y])) || [],
            "id": Number.isInteger(Number(active?.id)) ? undefined : active?.id
        };

        fetch('http://localhost:5050/save_region', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(values),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to save region');
            }
            return response.json();
        })
        .then(() => {
            notification.success({
                message: "Success",
                description: "Region saved successfully",
            });
        })
        .catch((error) => {
            notification.error({
                message: "Error",
                description: `Error: ${error.message}`,
            });
        });
    };

    return (
        <div>
            <Row>
                <Col span={10}>
                    <h1>Configuração de Região | SSA - Slag System | Aciaria | KR</h1>
                </Col>
                <Col span={4}>
                    <Button onClick={addRegion}>New Region</Button>
                </Col>
            </Row>

            <Row>
                <Col offset={1}>
                    <Button disabled={!active} onClick={() => edit()}>Edit</Button>
                </Col>
                <Col offset={1}>
                    <Button disabled={!active} onClick={() => resize()}>Resize</Button>
                </Col>
                <Col offset={1}>
                    <Button type="primary" disabled={!active} onClick={onSubmit}>Save</Button>
                </Col>
                <Col offset={1}>
                    <Button danger disabled={!active && !Number.isInteger((active as any)?.id)} onClick={onRemove}>Remove</Button>
                </Col>
            </Row>

            <FabricJSCanvas
                className={styles["fabric-canvas"]}
                onReady={onReady}
            />
        </div>
    );
};

// Utility function to calculate the distance from a point to a line
const distanceFromPointToLine = (point1: any, point2: any, targetPoint: any) => {
    const { x: x1, y: y1 } = point1;
    const { x: x2, y: y2 } = point2;
    const { x: x0, y: y0 } = targetPoint;

    const numerator = Math.abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1);
    const denominator = Math.sqrt(Math.pow(y2 - y1, 2) + Math.pow(x2 - x1, 2));

    return numerator / denominator;
};
