import grpc

from voltha_protos import voltha_pb2, voltha_pb2_grpc, device_pb2

# Indirizzo del server gRPC
server_address = 'localhost:55555'

def run():
    # Creazione di un canale gRPC
    channel = grpc.insecure_channel(server_address)

    # Creazione di uno stub gRPC
    stub = voltha_pb2_grpc.VolthaServiceStub(channel)

    device = device_pb2.Device()
    device.id = "my_device_id"
    device.type = "my_device_type"
    device.root = True
    device.parent_id = "parent_device_id"
    device.parent_port_no = 1
    device.vendor = "vendor_name"
    device.model = "model_name"
    device.hardware_version = "hw_version"
    device.firmware_version = "fw_version"
    device.serial_number = "serial123"
    device.vlan = 10
    device.mac_address = "00:11:22:33:44:55"
    device.ipv4_address = "192.168.1.1"

    device_id = voltha_pb2.ID()
    device_id.id = "my_device_id"

    response = stub.CreateDevice(device)

    #response = stub.GetDevice(device_id)
    
    #response = stub.DeleteDevice(device_id)

    print("Response received:\n", response)

if __name__ == '__main__':
    run()