PROGRAM analytic

    implicit none

    ! Namelist parameters 
    real :: CFL, dx, c, g, H, Lx, Lt
    namelist /params/ CFL, dx, c, g, H, Lx, Lt

    ! Variables 
    real :: dt
    integer :: Nx, Nt

    integer :: j, n
    real(8), allocatable :: h_now(:), u_now(:)
    character(len=100) :: filename
    real :: x, xr, xl

    ! Read namelist
    open(10, file="c)better-way/input.nml", status="old")
    read(10, nml=params)
    close(10)

    ! Compute derived values
    dt = CFL * dx / c
    Nx = int(Lx/dx)
    Nt = int(Lt/dt)

    ! Allocate one time slice
    allocate(h_now(Nx))
    allocate(u_now(Nx))

    ! Open file
    filename = "c)better-way/analytic.txt"
    open(10, file=filename, status="replace")

    ! ----------------------------
    ! Time loop
    ! ----------------------------
    DO n = 1, Nt

        DO j = 1, Nx

            x = (j-1)*dx

            xr = x - c*(n-1)*dt
            xl = x + c*(n-1)*dt

            ! periodic BC
            xr = xr - floor(xr)
            xl = xl - floor(xl)

            h_now(j) = 0.5*f(xr) + 0.5*f(xl)
            u_now(j) = (c/(2.0*H))*(f(xr) - f(xl))

        END DO

        ! write current timestep directly
        write(10, *) h_now

    END DO

    close(10)

    print *, "Simulation completed, saved as: ", filename 

contains

    ! Analytical shape function
    real function f(position)
        real, intent(in) :: position
        real, parameter :: pi = 4.0 * atan(1.0)

        if (position < 0.6 .AND. position > 0.4) then
            f = 0.5 + 0.5*cos(10*pi*(position-0.5))
        else
            f = 0.0
        end if
    end function f

END PROGRAM analytic