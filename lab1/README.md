# Реализация небольшой сети офиса
## Схема:
![image](https://github.com/medjed02/networks_hse/assets/58427105/62c90948-4163-46fb-afba-2066a7f2311e)

## VPC1
```
VPCS> set pcname VPC1
VPC1> ip 10.0.10.1/24 10.0.10.100
Checking for duplicate address...
VPC1 : 10.0.10.1 255.255.255.0 gateway 10.0.10.100
```

## VPC2
```
VPCS> set pcname VPC2
VPC2> ip 10.0.20.1/24 10.0.20.100
Checking for duplicate address...
VPC2 : 10.0.20.1 255.255.255.0 gateway 10.0.20.100
```

## Switch1
```
Switch>enable
Switch#configure terminal
Switch(config)#vlan 10
Switch(config-vlan)#exit
Switch(config)#vlan 20
Switch(config-vlan)#exit
Switch(config)#interface Gi0/0
Switch(config-if)#switchport mode access
Switch(config-if)#switchport access vlan 10
Switch(config-if)#exit

Switch(config)#interface range gigabitEthernet 0/1-2
Switch(config-if-range)#switchport trunk encapsulation dot1q
Switch(config-if-range)#switchport mode trunk
Switch(config-if-range)#switchport trunk allowed vlan 10,20
Switch(config-if-range)#exit
Switch(config)#exit

Switch#write memory
```

## Switch2
```
Switch>enable
Switch#configure terminal
Switch(config)#vlan 10
Switch(config-vlan)#exit
Switch(config)#vlan 20
Switch(config-vlan)#exit
Switch(config)#interface Gi0/0
Switch(config-if)#switchport mode access
Switch(config-if)#switchport access vlan 20
Switch(config-if)#exit

Switch(config)#interface range gigabitEthernet 0/1-2
Switch(config-if-range)#switchport trunk encapsulation dot1q
Switch(config-if-range)#switchport mode trunk
Switch(config-if-range)#switchport trunk allowed vlan 10,20
Switch(config-if-range)#exit
Switch(config)#exit

Switch#write memory
```

## Switch0
```
Switch>enable
Switch#configure terminal
Switch(config)#vlan 10
Switch(config-vlan)#exit
Switch(config)#vlan 20
Switch(config-vlan)#exit

Switch(config)#interface range gigabitEthernet 0/0-2
Switch(config-if-range)#switchport trunk encapsulation dot1q
Switch(config-if-range)#switchport mode trunk
Switch(config-if-range)#switchport trunk allowed vlan 10,20
Switch(config-if-range)#exit

Switch(config)#spanning-tree mode pvst
Switch(config)#spanning-tree extend system-id
Switch(config)#spanning-tree vlan 10,20 priority 0
Switch(config)#exit

Switch#write memory
```

## Router
```
Router>enable
Router#configure terminal
Router(config)#interface Gi0/0
Router(config-if)#no shutdown
Router(config-if)#exit

Router(config)#interface Gi0/0.10
Router(config-subif)#encapsulation dot1q 10
Router(config-subif)#ip address 10.0.10.100 255.255.255.0
Router(config-subif)#exit

Router(config)#interface Gi0/0.20
Router(config-subif)#encapsulation dot1q 20
Router(config-subif)#ip address 10.0.20.100 255.255.255.0
Router(config-subif)#exit
Router(config)#exit

Router#write memory
```
В итоге конфигурация получилась следующей:
```
Router#show ip int brief
Interface                  IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0         unassigned      YES unset  up                    up
GigabitEthernet0/0.10      10.0.10.100     YES manual up                    up
GigabitEthernet0/0.20      10.0.20.100     YES manual up                    up
GigabitEthernet0/1         unassigned      YES unset  administratively down down
GigabitEthernet0/2         unassigned      YES unset  administratively down down
GigabitEthernet0/3         unassigned      YES unset  administratively down down
```

## Проверка
Сперва немножко просто попингаем:

VPC1->VPC2
```
VPC1> ping 10.0.20.1

84 bytes from 10.0.20.1 icmp_seq=1 ttl=63 time=17.286 ms
84 bytes from 10.0.20.1 icmp_seq=2 ttl=63 time=11.304 ms
84 bytes from 10.0.20.1 icmp_seq=3 ttl=63 time=26.283 ms
84 bytes from 10.0.20.1 icmp_seq=4 ttl=63 time=16.661 ms
84 bytes from 10.0.20.1 icmp_seq=5 ttl=63 time=13.312 ms
```
VPC2->VPC1
```
VPC2> ping 10.0.10.1

84 bytes from 10.0.10.1 icmp_seq=1 ttl=63 time=16.739 ms
84 bytes from 10.0.10.1 icmp_seq=2 ttl=63 time=12.563 ms
84 bytes from 10.0.10.1 icmp_seq=3 ttl=63 time=11.151 ms
84 bytes from 10.0.10.1 icmp_seq=4 ttl=63 time=14.558 ms
84 bytes from 10.0.10.1 icmp_seq=5 ttl=63 time=15.634 ms
```

Посмотрим, что STP работает:

Switch1:
```
Switch#show spanning-tree vlan 10

VLAN0010
  Spanning tree enabled protocol ieee
  Root ID    Priority    10
             Address     5000.0005.0000
             Cost        4
             Port        3 (GigabitEthernet0/2)
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    32778  (priority 32768 sys-id-ext 10)
             Address     5000.0003.0000
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi0/0               Desg FWD 4         128.1    P2p
Gi0/1               Desg FWD 4         128.2    P2p
Gi0/2               Root FWD 4         128.3    P2p
```

```
Switch#show spanning-tree vlan 20

VLAN0020
  Spanning tree enabled protocol ieee
  Root ID    Priority    20
             Address     5000.0005.0000
             Cost        4
             Port        3 (GigabitEthernet0/2)
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    32788  (priority 32768 sys-id-ext 20)
             Address     5000.0003.0000
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi0/1               Desg FWD 4         128.2    P2p
Gi0/2               Root FWD 4         128.3    P2p
```

Switch2:
```
Switch>show spanning-tree vlan 10

VLAN0010
  Spanning tree enabled protocol ieee
  Root ID    Priority    10
             Address     5000.0005.0000
             Cost        4
             Port        3 (GigabitEthernet0/2)
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    32778  (priority 32768 sys-id-ext 10)
             Address     5000.0004.0000
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi0/1               Altn BLK 4         128.2    P2p
Gi0/2               Root FWD 4         128.3    P2p
```

```
VLAN0020
  Spanning tree enabled protocol ieee
  Root ID    Priority    20
             Address     5000.0005.0000
             Cost        4
             Port        3 (GigabitEthernet0/2)
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    32788  (priority 32768 sys-id-ext 20)
             Address     5000.0004.0000
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi0/0               Desg FWD 4         128.1    P2p
Gi0/1               Altn BLK 4         128.2    P2p
Gi0/2               Root FWD 4         128.3    P2p
```

Switch0:
```
Switch>show spanning-tree vlan 10

VLAN0010
  Spanning tree enabled protocol ieee
  Root ID    Priority    10
             Address     5000.0005.0000
             This bridge is the root
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    10     (priority 0 sys-id-ext 10)
             Address     5000.0005.0000
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi0/0               Desg FWD 4         128.1    P2p
Gi0/1               Desg FWD 4         128.2    P2p
Gi0/2               Desg FWD 4         128.3    P2p
```

```
Switch>show spanning-tree vlan 20

VLAN0020
  Spanning tree enabled protocol ieee
  Root ID    Priority    20
             Address     5000.0005.0000
             This bridge is the root
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    20     (priority 0 sys-id-ext 20)
             Address     5000.0005.0000
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi0/0               Desg FWD 4         128.1    P2p
Gi0/1               Desg FWD 4         128.2    P2p
Gi0/2               Desg FWD 4         128.3    P2p
```

Видим, что линк между коммутаторами уровня доступ заблокировался, а коммутатор уровня распределения стал корневым.

Теперь отключим связь между Switch1 и Switch2 (я просто заблокировал Gi0/1 на Switch2) и проверим пинги снова:
```
Switch>enable
Switch#configure terminal
Switch(config)#interface Gi0/1
Switch(config-if)#shutdown
Switch(config-if)#exit
Switch(config)#exit
Switch#exit
```

VPC1->VPC2
```
VPC1> ping 10.0.20.1

84 bytes from 10.0.20.1 icmp_seq=1 ttl=63 time=20.321 ms
84 bytes from 10.0.20.1 icmp_seq=2 ttl=63 time=24.008 ms
84 bytes from 10.0.20.1 icmp_seq=3 ttl=63 time=11.298 ms
84 bytes from 10.0.20.1 icmp_seq=4 ttl=63 time=13.353 ms
84 bytes from 10.0.20.1 icmp_seq=5 ttl=63 time=14.825 ms
```

VPC2->VPC1
```
VPC2> ping 10.0.10.1

84 bytes from 10.0.10.1 icmp_seq=1 ttl=63 time=23.106 ms
84 bytes from 10.0.10.1 icmp_seq=2 ttl=63 time=13.942 ms
84 bytes from 10.0.10.1 icmp_seq=3 ttl=63 time=14.289 ms
84 bytes from 10.0.10.1 icmp_seq=4 ttl=63 time=15.599 ms
84 bytes from 10.0.10.1 icmp_seq=5 ttl=63 time=16.926 ms
```
