PROGRAM leapfrogUnstagg

    implicit none


    ! Namelist parameters 
    real :: CFL, dx, c, g, H, Lx, Lt
    namelist /params/ CFL, dx, c, g, H, Lx, Lt

    ! Variables
    real :: dt
    integer :: Nx, Nt

    integer :: j, n
    real :: x
    real(8), allocatable :: h_old(:), h_now(:), h_new(:)
    real(8), allocatable :: u_old(:), u_now(:), u_new(:)
    character(len=100) :: filename
    real, parameter :: pi = 4.0 * atan(1.0)

    ! Read namelist
    open(10, file="c)better-way/input.nml", status="old")
    read(10, nml=params)
    close(10)

    ! Compute derived values
    dt = CFL * dx / c
    Nx = int(Lx/dx)
    Nt = int(Lt/dt)

    ! Allocate arrays
    allocate(h_old(Nx), h_now(Nx), h_new(Nx))
    allocate(u_old(Nx), u_now(Nx), u_new(Nx))

    ! Open file
    filename = "c)better-way/unstagg.txt"
    open(10, file=filename, status="replace")


    ! ----------------------------
    ! The actual code
    ! ----------------------------

    ! Initialize (n = 1)
    u_old = 0.0

    DO j = 1, Nx
        x = (j-1)*dx
        if (x < 0.6 .AND. x > 0.4) then
            h_old(j) = 0.5 + 0.5*cos(10*pi*(x-0.5))
        else
            h_old(j) = 0.0
        end if
    END DO

    write(10, *) h_old ! Save


    ! First step (Forward Euler)
    DO j = 1, Nx
        if (j == 1) then
            h_now(j) = h_old(j) - (H*dt/(2*dx)) * (u_old(j+1) - u_old(Nx))
            u_now(j) = u_old(j) - (g*dt/(2*dx)) * (h_old(j+1) - h_old(Nx))

        else if (j == Nx) then
            h_now(j) = h_old(j) - (H*dt/(2*dx)) * (u_old(1) - u_old(j-1))
            u_now(j) = u_old(j) - (g*dt/(2*dx)) * (h_old(1) - h_old(j-1))

        else
            h_now(j) = h_old(j) - (H*dt/(2*dx)) * (u_old(j+1) - u_old(j-1))
            u_now(j) = u_old(j) - (g*dt/(2*dx)) * (h_old(j+1) - h_old(j-1))
        end if
    END DO

    write(10, *) h_now ! Save


    ! Leapfrog time stepping
    DO n = 2, Nt-1

        DO j = 1, Nx
            if (j == 1) then
                h_new(j) = h_old(j) - (H*dt/dx) * (u_now(j+1) - u_now(Nx))
                u_new(j) = u_old(j) - (g*dt/dx) * (h_now(j+1) - h_now(Nx))

            else if (j == Nx) then
                h_new(j) = h_old(j) - (H*dt/dx) * (u_now(1) - u_now(j-1))
                u_new(j) = u_old(j) - (g*dt/dx) * (h_now(1) - h_now(j-1))

            else
                h_new(j) = h_old(j) - (H*dt/dx) * (u_now(j+1) - u_now(j-1))
                u_new(j) = u_old(j) - (g*dt/dx) * (h_now(j+1) - h_now(j-1))
            end if
        END DO

        ! Shift time levels
        h_old = h_now
        h_now = h_new

        u_old = u_now
        u_now = u_new

        write(10, *) h_now ! Save

    END DO

    close(10)

    print *, "Simulation completed, saved as: ", filename 

END PROGRAM leapfrogUnstagg