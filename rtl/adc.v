`ifdef ADC_V
`define ADC_V

    module adc #(parameter INPUT_WIDTH, OUTPUT_WIDTH) (
        input                      clk,
        input                      rst_n,
        input                      valid_in,
        input  [INPUT_WIDTH-1:0]   ADC_i,
        input  [INPUT_WIDTH-1:0]   ADC_q,
        output [OUTPUT_WIDTH-1:0]  rx_i,
        output [OUTPUT_WIDTH-1:0]  rx_q,
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
                rx_i <= ADC_i;
                rx_q <= ADC_q;
                valid_out = VALID;
            end
            else begin
                rx_i <= ADC_i;
                rx_q <= ADC_q;
                valid_out <= valid_out;
            end
        end
    endmodule
`endif