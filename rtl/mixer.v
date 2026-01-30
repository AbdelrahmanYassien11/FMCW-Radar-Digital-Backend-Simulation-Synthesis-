`ifdef MIXER_V
`define MIXER_V

    module mixer #(parameter INPUT_WIDTH, OUTPUT_WIDTH) (
        input                      clk,
        input                      rst_n,
        input                      valid_in,
        input  [INPUT_WIDTH-1:0]   tx_i, // NCO in hardware
        input  [INPUT_WIDTH-1:0]   tx_q, // NCO in hardware
        input  [OUTPUT_WIDTH-1:0]  rx_i, // ADC Sample in hardware
        input  [OUTPUT_WIDTH-1:0]  rx_q, // ADC Sample in hardware
        output [OUTPUT_WIDTH-1:0]  beat_i, // Beat Signal
        output [OUTPUT_WIDTH-1:0]  beat_q, // Beat Signal
        output                     valid_out
    );

    localparam VALID = 1, INVALID = 0;
    
        always@(negedge rst_n or posedge clk) begin
            if(~rst_n) begin
                rx_i <= 0;
                rx_q <= 0;
                valid_out <= INVALID;
            end
            else if(valid_in) begin
                beat_i <= tx_i * rx_i + tx_q * rx_q;
                beat_q <= tx_q * rx_i - tx_i * rx_q;
                valid_out <= 1;
            end
            else begin
                beat_i <= beat_i;
                beat_q <= beat_q;
                valid_out <= valid_out;
            end
        end
    endmodule
`endif