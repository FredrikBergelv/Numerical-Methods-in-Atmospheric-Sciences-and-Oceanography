PROGRAM lec_02
  implicit none

  ! Declaration of variables
  real(8), parameter :: pi = 4.0 * ATAN(1.0)
  real(8) :: pi_read

  ! Open unit (create file) & write
  ! Open
  open(10, FILE = "writing-PI.dat", status = "replace")
  
  ! Write in file
  write(10, *) pi
  write(*, *) pi          ! Write in terminal
  write(10, "(f12.6)") pi
  write(*, "(f12.6)") pi

  !close file
  close(10)

  ! Open again and read the data
  open(10, FILE = "writing-PI.dat", status = "old", position="rewind")
  read(10, "(f12.4)") pi_read
  write(*, "(f12.4)") pi_read
  read(10,*) pi_read
  write(*,*) pi_read

  close(100)

END PROGRAM lec_02