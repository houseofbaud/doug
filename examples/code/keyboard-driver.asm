.global _start

.section .data

key_buffer:
  .space 256           # allocate space for keyboard buffer

.section .text

_start:
  movq %rsp, %rbp      # set up stack frame
  andq $-16, %rsp      # align stack pointer to 16-byte boundary

  # initialize interrupt handlers and set up keyboard buffer
  movq $key_buffer, %rdi
  movq $256, %rsi
  call init_keyboard

  # main loop: wait for input
  call read_char
  # do something with input character
  jmp main_loop

# subroutine to initialize keyboard interrupts and buffer
init_keyboard:
  # set up keyboard interrupt handler
  pushq %rax
  pushq %rdx
  movq $0x21, %rax
  movq keyboard_interrupt, %rdx
  int $0x80
  popq %rdx
  popq %rax

  # set up buffer
  movq $0x21, %rax
  movq $key_buffer, %rdx
  int $0x80

  ret

# interrupt handler for keyboard input
keyboard_interrupt:
  pushq %rax
  pushq %rbx

  # read input from keyboard buffer and store in key_buffer
  movq $0x21, %rax
  movq $key_buffer, %rbx
  int $0x80

  popq %rbx
  popq %rax
  iretq               # return from interrupt

# subroutine to read a single character from keyboard buffer
read_char:
  pushq %rbx
  movq $0x21, %rax    # read from keyboard buffer
  movq $key_buffer, %rbx
  int $0x80
  popq %rbx
  ret

main_loop:
  # do some other stuff here
  jmp main_loop
