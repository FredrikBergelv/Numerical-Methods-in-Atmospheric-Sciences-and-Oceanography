PROGRAM array

    implicit none
    integer, parameter :: Nx=41
    integer :: ii
    real(4) :: dx = 0.25 
    real(4), dimension(Nx) :: x  ! Starts from x(1), x(2), etc

    do ii = 1, Nx
        x(ii) = (ii-1) * dx
    end do

    print '(F10.4)', x

END PROGRAM array