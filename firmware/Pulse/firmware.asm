; firmware/pulse/firmware.bin
; пример прошивки для Pulse CPU
; не забывайте что опкоды есть в docs.md

start:
    movi r1, 100      ; r1 = 100
    movi r2, 50       ; r2 = 50
    add r3, r1        ; r3 = r1 + r2
    mul r4, r3        ; r4 = r3 * r2
    
    push r1           ; сохраняем r1 в стеке
    push r2
    
    call draw_screen  ; вызываем функцию
    
    pop r2            ; восстанавливаем
    pop r1
    
    load_frame        ; загрузить кадр видео
    
    jmp start         ; бесконечный цикл

draw_screen:
    ; код отрисовки OSD
    movi r5, 0xFFFF
    store 0x8000, r5  ; запись в видеопамять
    ret

halt:
    halt
