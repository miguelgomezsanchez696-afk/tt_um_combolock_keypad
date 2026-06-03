`default_nettype none

module seven_seg_decoder (
    input  wire [3:0] value,
    output reg  [6:0] segments
);

    // Active-high segments, packed as {g, f, e, d, c, b, a}.
    always @(*) begin
        case (value)
            4'h0: segments = 7'h3f;
            4'h1: segments = 7'h06;
            4'h2: segments = 7'h5b;
            4'h3: segments = 7'h4f;
            4'h4: segments = 7'h66;
            4'h5: segments = 7'h6d;
            4'h6: segments = 7'h7d;
            4'h7: segments = 7'h07;
            4'h8: segments = 7'h7f;
            4'h9: segments = 7'h6f;
            4'ha: segments = 7'h77;
            4'hb: segments = 7'h7c;
            4'hc: segments = 7'h39;
            4'hd: segments = 7'h5e;
            4'he: segments = 7'h79;
            4'hf: segments = 7'h71;
            default: segments = 7'h00;
        endcase
    end

endmodule

`default_nettype wire
