PROGRAM analyticA

    implicit none

    real, parameter :: CFL = 0.9

    real, parameter :: dx=0.0125, c=1.0, g=1.0, H=1.0
    real, parameter :: dt = CFL * dx / c
    real, parameter :: Lx=1.0, Lt=10.0
    integer, parameter :: Nx = INT(Lx/dx), Nt = INT(Lt/dt)

    integer :: j, n
    real(8), dimension(Nt, Nx) :: h_array, u_array
    character(len=50) :: filename
    real :: x, xr, xl

    ! analytical solution
    DO n = 1, Nt
        DO j = 1, Nx
            x = (j-1)*dx

            ! right-moving wave
            xr = x - c*(n-1)*dt

            ! left-moving wave
            xl = x + c*(n-1)*dt

            ! periodic BC
            xr = xr - FLOOR(xr)
            xl = xl - FLOOR(xl)

            ! build solution from two travelling waves
            h_array(n,j) = 0.5*f(xr) + 0.5*f(xl)

            u_array(n,j) = (c*0.5/H)*f(xr) - (c*0.5/H)*f(xl)

        END DO
    END DO



    ! write files
    write(filename, '(A,F4.2,A)') 'b)staggered/h-analytic.txt'    
    open(10, file=filename, status="replace")
    do n = 1, Nt
        write(10, *) h_array(n, :)
    end do
    close(10)

    write(filename, '(A,F4.2,A)') 'b)staggered/u-analytic.txt'
    open(11, file=filename, status="replace")
    do n = 1, Nt
        write(11, *) u_array(n, :)
    end do
    close(11)

    print *, "Simulation completed. Results written to ", filename

    ! analytical solution function
    contains
        real function f(position)
            real, intent(in) :: position
            real, parameter :: pi = 4.0 * ATAN(1.0)

            if (position < 0.6 .AND. position > 0.4) then
                f = 0.5 + 0.5*cos(10*pi*(position-0.5))
            else
                f = 0.0
            end if
        end function f

END PROGRAM analyticA