import './App.css';
import { App, ConfigProvider, Layout, Menu, Typography, Button, notification } from 'antd';
import { PublicRoute } from './components/router/PublicRoute';
import { PrivateRoute } from './components/router/PrivateRoute';
import { LoginPage } from './pages/auth/Login';
import { useAuthToken } from './hooks/auth/useAuthToken';
import { useEffect, useState } from 'react';
import { Switch, useLocation } from 'wouter';
import { FeatureConfig } from './pages/camera/FeatureConfig';
import { CameraPage } from './pages/camera/CameraPage';

const { Header, Content } = Layout;
const { Title } = Typography;

function BackOffice() {
  const token = useAuthToken();
  const [location, setLocation] = useLocation();
  const [isRecording, setIsRecording] = useState(false);
  const [isRaceRunning, setIsRaceRunning] = useState(false);
  const [videoUrl, setVideoUrl] = useState<string | null>(null); // URL do vídeo selecionado

  const menuItems = [
    {
      key: '1',
      label: 'Cameras',
      onClick: () => setLocation('/s/camera'),
    },
    {
      key: '2',
      label: 'Editar Região',
      onClick: () => setLocation('/s/area-config'),
    },
  ];

  const handleToggleRecording = () => {
    setIsRecording(!isRecording);
  };

  const handleToggleRace = () => {
    setIsRaceRunning(!isRaceRunning);
  };

  useEffect(() => {
    if (window.location.pathname === "/login") {
      return;
    }
    if (!token) {
      window.location.href = "/login";
    }
  }, [token]);

  // Função para lidar com o carregamento do vídeo
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
    <ConfigProvider>
      <App>
        <div className="App">
          <Switch>
            <PublicRoute path="/login" component={LoginPage} />
            {token && (
              <Layout style={{ height: '100vh'}}>
                <Header
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    backgroundColor: '#ff4400',
                    height: '70px',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', flex: '1 0 auto' }}>
                    <Title style={{ color: 'white', margin: 0, paddingRight: '20px', whiteSpace: 'nowrap', fontSize: 'small' }}>
                      SSA - Slag Skimming Assistant
                    </Title>
                    <Menu
                      theme="dark"
                      mode="horizontal"
                      defaultSelectedKeys={['1']}
                      items={menuItems}
                      style={{
                        background: 'transparent',
                        flex: '1 0 auto',
                        justifyContent: 'flex-start',
                      }}
                    />
                  </div>
                  <div style={{ display: 'flex', gap: '10px' }}>
                  <Button
                    onClick={() => document.getElementById('videoUploadInput')?.click()}
                    style={{ fontSize: '2rem' }} // Herda o tamanho da fonte do contêiner pai
                  >
                      Carregar Vídeo
                  </Button>
                    <Button type="primary" onClick={handleToggleRace} className='orange-button'>
                      {isRaceRunning ? 'Parar Corrida' : 'Começar Corrida'}
                    </Button>
                    <Button type="primary" onClick={handleToggleRecording} className='orange-button'>
                      {isRecording ? 'Parar Gravação' : 'Gravar Corrida'}
                    </Button>
                  </div>
                </Header>

                <Content className="Content">
                  <PrivateRoute path="/s/area-config/" component={FeatureConfig} />
                  <PrivateRoute path="/s/camera/:cameraid?" component={CameraPage} />
                </Content>
              </Layout>
            )}
          </Switch>
        </div>
      </App>
    </ConfigProvider>
  );
}

export default BackOffice;
