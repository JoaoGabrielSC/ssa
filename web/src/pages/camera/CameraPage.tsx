import React, { useRef, useState } from "react";
import { Button, notification } from "antd";
import styles from "./CameraPage.module.scss";

export const CameraPage = () => {
    const videoRef = useRef<HTMLVideoElement | null>(null); // Referência ao elemento de vídeo
    const [videoUrl, setVideoUrl] = useState<string | null>(null); // URL do vídeo selecionado

    const handleVideoUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            const url = URL.createObjectURL(file); // Gera uma URL temporária para o vídeo
            setVideoUrl(url); // Armazena a URL para ser usada no player
        } else {
            notification.error({
                message: 'Erro',
                description: 'Não foi possível carregar o vídeo.',
            });
        }
    };

    return (
        <div className={styles.container}>
            <div className={styles.videoContainer}>
                <video
                    ref={videoRef}
                    src={videoUrl || undefined}
                    width="720"
                    height="480"
                    controls
                    className={styles.video}
                />
            </div>
            <div className={styles.chartContainer}>
                <canvas />
            </div>
            <div>
                <input
                    type="file"
                    accept="video/mp4" // Aceita apenas arquivos MP4
                    onChange={handleVideoUpload}
                    style={{ display: 'none' }} // Esconde o input de arquivo
                    id="videoUploadInput"
                />
                {/* <Button onClick={() => document.getElementById('videoUploadInput')?.click()}>
                    Carregar Vídeo
                </Button> */}
            </div>
        </div>
    );
};
