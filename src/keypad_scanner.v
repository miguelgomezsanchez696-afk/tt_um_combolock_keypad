`default_nettype none

module keypad_scanner (
    input  wire       clk,
    input  wire       rst_n,
    input  wire [3:0] cols,
    output wire [3:0] rows,
    output reg        key_valid,
    output reg  [3:0] key_code,
    output reg        key_star,
    output reg        key_hash
);

    reg [1:0] scan_row;
    reg       key_down;
    reg       any_pressed_in_scan;

    wire [3:0] col_pressed = ~cols;
    wire       pressed = |col_pressed;
    wire       saw_pressed = any_pressed_in_scan | pressed;

    assign rows = ~(4'b0001 << scan_row);

    function [3:0] decode_key;
        input [1:0] row;
        input [3:0] col;
        begin
            case ({row, col})
                6'b00_0001: decode_key = 4'h1;
                6'b00_0010: decode_key = 4'h2;
                6'b00_0100: decode_key = 4'h3;
                6'b00_1000: decode_key = 4'ha;
                6'b01_0001: decode_key = 4'h4;
                6'b01_0010: decode_key = 4'h5;
                6'b01_0100: decode_key = 4'h6;
                6'b01_1000: decode_key = 4'hb;
                6'b10_0001: decode_key = 4'h7;
                6'b10_0010: decode_key = 4'h8;
                6'b10_0100: decode_key = 4'h9;
                6'b10_1000: decode_key = 4'hc;
                6'b11_0001: decode_key = 4'he; // *
                6'b11_0010: decode_key = 4'h0;
                6'b11_0100: decode_key = 4'hf; // #
                6'b11_1000: decode_key = 4'hd;
                default:    decode_key = 4'h0;
            endcase
        end
    endfunction

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            scan_row            <= 2'd0;
            key_down            <= 1'b0;
            any_pressed_in_scan <= 1'b0;
            key_valid           <= 1'b0;
            key_code            <= 4'h0;
            key_star            <= 1'b0;
            key_hash            <= 1'b0;
        end else begin
            key_valid <= 1'b0;
            key_star  <= 1'b0;
            key_hash  <= 1'b0;

            if (pressed && !key_down) begin
                key_valid <= 1'b1;
                key_code  <= decode_key(scan_row, col_pressed);
                key_star  <= (scan_row == 2'd3) && col_pressed[0];
                key_hash  <= (scan_row == 2'd3) && col_pressed[2];
                key_down  <= 1'b1;
            end

            if (scan_row == 2'd3) begin
                any_pressed_in_scan <= 1'b0;
                if (!saw_pressed) begin
                    key_down <= 1'b0;
                end
            end else begin
                any_pressed_in_scan <= saw_pressed;
            end

            scan_row <= scan_row + 2'd1;
        end
    end

endmodule

`default_nettype wire
