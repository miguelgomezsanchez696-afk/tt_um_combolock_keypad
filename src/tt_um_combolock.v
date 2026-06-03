`default_nettype none

module tt_um_combolock #(
    parameter integer LOCKOUT_CYCLES = 1024
) (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    // uio[3:0]  : keypad rows, active-low outputs from ASIC
    // uio[7:4]  : keypad columns, active-low inputs to ASIC
    //
    // uo_out[6:0]: active-high 7-segment output for the entered hex digit
    //               bit order is {g, f, e, d, c, b, a} as a packed value,
    //               so uo_out[0] drives segment a and uo_out[6] drives g.
    // uo_out[7]  : decimal point, used as temporary lockout indicator

    reg [3:0] password;
    reg [3:0] entered_code;
    reg [1:0] attempts;
    reg       unlocked;
    reg       locked_out;
    reg [15:0] lockout_timer;

    localparam [15:0] LOCKOUT_TIMER_RELOAD = LOCKOUT_CYCLES;

    wire [3:0] keypad_rows;
    wire       key_valid;
    wire [3:0] key_code;
    wire       key_star;
    wire       key_hash;
    wire [6:0] seven_seg;

    keypad_scanner keypad_scanner_i (
        .clk(clk),
        .rst_n(rst_n),
        .cols(uio_in[7:4]),
        .rows(keypad_rows),
        .key_valid(key_valid),
        .key_code(key_code),
        .key_star(key_star),
        .key_hash(key_hash)
    );

    wire code_key = key_valid && !key_star && !key_hash;
    wire enter    = key_valid && key_hash;
    wire set_pass = key_valid && key_star;

    seven_seg_decoder seven_seg_decoder_i (
        .value(entered_code),
        .segments(seven_seg)
    );

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            password     <= 4'b0000;
            entered_code <= 4'b0000;
            attempts     <= 2'd0;
            unlocked     <= 1'b0;
            locked_out   <= 1'b0;
            lockout_timer <= 16'd0;
        end else if (locked_out) begin
            unlocked <= 1'b0;

            if (lockout_timer <= 16'd1) begin
                locked_out   <= 1'b0;
                attempts     <= 2'd0;
                lockout_timer <= 16'd0;
            end else begin
                lockout_timer <= lockout_timer - 16'd1;
            end
        end else if (ena) begin
            if (code_key) begin
                entered_code <= key_code;
            end

            if (set_pass && !locked_out) begin
                password      <= entered_code;
                attempts      <= 2'd0;
                unlocked      <= 1'b0;
                lockout_timer <= 16'd0;
            end else if (enter && !locked_out) begin
                if (entered_code == password) begin
                    attempts      <= 2'd0;
                    unlocked      <= 1'b1;
                    lockout_timer <= 16'd0;
                end else begin
                    unlocked <= 1'b0;
                    if (attempts == 2'd2) begin
                        attempts      <= 2'd3;
                        locked_out    <= 1'b1;
                        lockout_timer <= LOCKOUT_TIMER_RELOAD;
                    end else begin
                        attempts <= attempts + 2'd1;
                    end
                end
            end
        end
    end

    assign uo_out = {locked_out, seven_seg};

    assign uio_out = {4'b0000, keypad_rows};
    assign uio_oe  = 8'b0000_1111;

    wire _unused = &{ui_in, uio_in[3:0], unlocked, 1'b0};

endmodule

`default_nettype wire
