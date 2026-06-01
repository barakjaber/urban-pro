import struct, zlib, os, math

def make_icon(size):
    W = H = size
    BG  = (201, 169, 110)   # gold
    FG  = (10,  10,  10)    # dark letter
    OUT = (10,  10,  10)    # outside circle

    cx, cy = W / 2.0, H / 2.0
    r_outer = W * 0.46
    r_inner = W * 0.30

    pixels = [[OUT] * W for _ in range(H)]

    # Gold circle background
    for y in range(H):
        for x in range(W):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r_outer ** 2:
                pixels[y][x] = BG

    # Draw "U" letter centred in the circle
    s = size / 192.0
    bar_w   = max(2, int(20 * s))
    total_w = int(80 * s)
    bar_h   = int(90 * s)
    bot_h   = max(2, int(20 * s))

    lx = int(cx - total_w / 2)
    rx = int(cx + total_w / 2) - bar_w
    ty = int(cy - bar_h / 2)

    for y in range(H):
        for x in range(W):
            in_left  = lx <= x < lx + bar_w and ty <= y < ty + bar_h
            in_right = rx <= x < rx + bar_w and ty <= y < ty + bar_h
            in_bot   = lx <= x < rx + bar_w and ty + bar_h - bot_h <= y < ty + bar_h
            if in_left or in_right or in_bot:
                # Only draw inside the gold circle
                if (x - cx) ** 2 + (y - cy) ** 2 <= r_outer ** 2:
                    pixels[y][x] = FG

    # Encode as RGB PNG
    raw = b''
    for row in pixels:
        raw += b'\x00'
        for r, g, b in row:
            raw += bytes([r, g, b])

    compressed = zlib.compress(raw, 6)

    def chunk(tag, data):
        body = tag + data
        return struct.pack('>I', len(data)) + body + struct.pack('>I', zlib.crc32(body) & 0xFFFFFFFF)

    ihdr = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
    return (
        b'\x89PNG\r\n\x1a\n'
        + chunk(b'IHDR', ihdr)
        + chunk(b'IDAT', compressed)
        + chunk(b'IEND', b'')
    )

os.makedirs('icons', exist_ok=True)
for size in [192, 512]:
    data = make_icon(size)
    path = f'icons/icon-{size}.png'
    with open(path, 'wb') as f:
        f.write(data)
    print(f'Created {path}  ({len(data):,} bytes)')
