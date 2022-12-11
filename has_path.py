def has_path(self, x1, y1, x2, y2):
    """Метод для определения доступности из клетки (x1, y1)
     клетки (x2, y2) по волновому методу"""
    # словарь расстояний
    d = {(x1, y1): 0}
    v = [(x1, y1)]
    while len(v) > 0:
        x, y = v.pop(0)
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx * dy != 0:
                    continue
                if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                    continue
                if self.board[y + dy][x + dx] == 10:
                    dn = d.get((x + dx, y + dy), -1)
                    if dn == -1:
                        d[(x + dx, y + dy)] = d.get((x, y), -1) + 1
                        v.append((x + dx, y + dy))
    dist = d.get((x2, y2), -1)
    return dist >= 0

