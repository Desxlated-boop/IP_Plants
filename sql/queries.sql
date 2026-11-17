-- name: plants_list
-- Все растения с владельцем и местом (LEFT JOIN сохраняет необязательные связи).
SELECT p.id, p.name, p.species, p.interval_days, p.last_watered,
       o.name AS owner, l.name AS location
FROM plants p LEFT JOIN owners o ON o.id = p.owner_id
LEFT JOIN locations l ON l.id = p.location_id ORDER BY p.name;

-- name: watering_list
-- Журнал поливов с названиями растений.
SELECT w.id, w.watered_on, p.name AS plant, w.note
FROM waterings w JOIN plants p ON p.id = w.plant_id
ORDER BY w.watered_on DESC, w.id DESC;

-- name: due_on_date
-- Растения, которым нужен полив к выбранной дате.
SELECT id, name, last_watered, interval_days,
       date(last_watered, '+' || interval_days || ' days') AS next_watering
FROM plants WHERE date(last_watered, '+' || interval_days || ' days') <= date(?)
ORDER BY next_watering, name;

-- name: plants_by_light
-- Растения по уровню освещения.
SELECT p.name, l.name AS location, l.light FROM plants p
JOIN locations l ON l.id = p.location_id WHERE l.light = ? ORDER BY p.name;

-- name: watering_details
-- Поливы с растением и его владельцем.
SELECT w.watered_on, p.name AS plant, o.name AS owner
FROM waterings w JOIN plants p ON p.id = w.plant_id
LEFT JOIN owners o ON o.id = p.owner_id ORDER BY w.watered_on DESC;

-- name: plant_details
-- Растения со связанными владельцами и местами.
SELECT p.name, o.name AS owner, l.name AS location FROM plants p
LEFT JOIN owners o ON o.id = p.owner_id
LEFT JOIN locations l ON l.id = p.location_id ORDER BY p.id;

-- name: plant_total
-- Общее количество растений.
SELECT COUNT(*) AS total FROM plants;

-- name: watering_total
-- Общее количество записей журнала.
SELECT COUNT(*) AS total FROM waterings;

-- name: plants_by_owner
-- Количество растений у каждого владельца, включая владельцев без растений.
SELECT o.name, COUNT(p.id) AS total FROM owners o
LEFT JOIN plants p ON p.owner_id = o.id GROUP BY o.id, o.name ORDER BY o.name;

-- name: plants_by_location
-- Количество растений в каждом месте, включая пустые места.
SELECT l.name, COUNT(p.id) AS total FROM locations l
LEFT JOIN plants p ON p.location_id = l.id GROUP BY l.id, l.name ORDER BY l.name;

-- name: watering_by_plant
-- Растения с числом поливов не меньше заданного.
SELECT p.name, COUNT(w.id) AS total FROM plants p
LEFT JOIN waterings w ON w.plant_id = p.id GROUP BY p.id, p.name
HAVING COUNT(w.id) >= ? ORDER BY total DESC, p.name;

-- name: recent_waterings
-- Последние записи с ограничением и сдвигом.
SELECT w.watered_on, p.name AS plant FROM waterings w
JOIN plants p ON p.id = w.plant_id ORDER BY w.watered_on DESC LIMIT ? OFFSET ?;
