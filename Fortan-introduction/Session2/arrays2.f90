PROGRAM array

    implicit none
    integer :: Nx
    integer :: ii
    real(4) :: dx = 0.25, Lx=1

    real(4), dimension(:), allocatable :: x 

    Nx = int(Lx/dx) + 1

    allocate(x(Nx))

    do ii = 1, Nx
        x(ii) = (ii-1) * dx
    end do

    print '(F10.4)', x

END PROGRAM array