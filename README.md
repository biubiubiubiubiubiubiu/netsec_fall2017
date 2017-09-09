# netsec_fall2017

The repository for the 2017 Fall JHU Network Security Project

* Some explanation on PacketType.Deserializer()
    * If the terminal receives message with several Packet classes together, it will take every k Bytes in every loop, and update the bytes it received with "update()" method. Then, if the deserializer can deserialize a Packet object from the updated received message, we can use "nextPackets()" method to get a Packet from deserialized result.

* For lab_1b, cd into lab_1b and run:
    ```
    $ python3 submission.py
    ```

* For lab_1c, cd into lab_1c and run:
    ```
    $ python3 submission.py
    ```