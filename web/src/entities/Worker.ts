export class Worker {
    public camera_id: string;
    public gas_station_id: string;
    public gas_station_name: string;

    constructor(camera_id: string, gas_station_id: string, gas_station_name: string) {
        this.camera_id = camera_id;
        this.gas_station_id = gas_station_id;
        this.gas_station_name = gas_station_name;
    }
}
