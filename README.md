# hls_abmof_tools
Tools for ABMOF Vivado HLS project

The java file is used to generate the .txt files including events and its corresponding OF GT.
Two python scripts are used to convert OF GT txt files to .bin files. 

The difference between 
them is that one is only for Vivado HLS GT testbench because in this conversion, one event 
will be converted to 3x4Byte rather than the standard 2x4Byte. 

The reason why it has one extra
Byte is because this extra Byte is used for representing OF GT. 

For EFAST/SFAST testbench GT file,
the standard conversion is enough since corner for GT only occupy one bit and it could be placed on
the LSB of the Address.
