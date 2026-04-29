PROGRAM Cgrid

    implicit none

    ! Namelist parameters 
    real :: CFL, f, dx, dy, g, H0, Lx, Ly, Lt, alpha
    namelist /params/ CFL, f, dx, dy, g, H0, Lx, Ly, Lt, alpha

    ! Variables 
    real :: dt
    integer :: Nx, Ny, Nt

    integer :: i, j, n, ip, im, jp, jm
    real :: x, y
    real(8), allocatable :: h(:,:,:), u(:,:,:), v(:,:,:)
    character(len=100) :: filename
    real, parameter :: pi = 4.0 * atan(1.0)

    ! Read namelist
    open(10, file="2D-SWE/input.nml", status="old")
    read(10, nml=params)
    close(10)

    ! Compute derived values
    dt = CFL / ( sqrt(g*H0) * sqrt( (1/dx**2) + (1/dy**2) ) )
    Nx = int(Lx/dx)
    Ny = int(Ly/dy)
    Nt = int(Lt/dt)

    ! Allocate arrays
    allocate(h(Nx,Ny,3), u(Nx,Ny,3), v(Nx,Ny,3))

    ! Open file for svaing
    filename = "2D-SWE/h_array.txt"
    open(10, file=filename, status="replace")


    ! ----------------------------
    ! The actual code
    ! ----------------------------

    ! Initialize (n = 1)
    u(:,:,1) = 0.0
    v(:,:,1) = 0.0


    DO j = 1, Ny
        do i = 1, Nx
            x = (i-1)*dx
            y = (j-1)*dy
            if (x < 0.6 .AND. x > 0.4 .AND. y < 0.6 .AND. y > 0.4) then
                h(i,j,1) = exp(-((x-0.5)**2 + (y-0.5)**2)/0.01)
            else
                h(i,j,1) = 0.0
            end if
        end do
    END DO

    write(10, *) h(:,:,1) ! Save


    ! First step (Forward Euler)
    DO j = 1, Ny
        DO i = 1, Nx
            
            ! Apply cyclic B.C.
            ip = i + 1
            im = i - 1
            jp = j + 1
            jm = j - 1

            if (i == Nx) ip = 1
            if (i == 1)  im = Nx
            if (j == Ny) jp = 1
            if (j == 1)  jm = Ny

            ! Do the Euler forward 
            h(i,j,2) = h(i,j,1) - H0*dt * ((u(i,j,1)-u(im,j,1))/dx + (v(i,j,1)-v(i,jm,1))/dy)
            u(i,j,2) = u(i,j,1) + dt * (-g*(h(ip,j,1)-h(i,j,1))/dx + f*(v(i,j,1)+v(ip,j,1)+v(ip,jm,1)+v(i,jm,1))/4)
            v(i,j,2) = v(i,j,1) + dt * (-g*(h(i,jp,1)-h(i,j,1))/dy - f*(u(i,j,1)+u(i,jp,1)+u(im,jp,1)+u(im,j,1))/4)

        END DO
    END DO

    write(10, *) h(:,:,2) ! Save

    ! Leapfrog time stepping
    DO n = 2, Nt-1

        DO j = 1, Ny
            DO i = 1, Nx
            
            ! Apply cyclic B.C.
            ip = i + 1
            im = i - 1
            jp = j + 1
            jm = j - 1

            if (i == Nx) ip = 1
            if (i == 1)  im = Nx
            if (j == Ny) jp = 1
            if (j == 1)  jm = Ny

            ! Do the Leapfrog  
            h(i,j,3) = h(i,j,1) - 2*H0*dt * ((u(i,j,2)-u(im,j,2))/dx + (v(i,j,2)-v(i,jm,2))/dy)
            u(i,j,3) = u(i,j,1) + 2*dt * (-g*(h(ip,j,2)-h(i,j,2))/dx + f*(v(i,j,2)+v(ip,j,2)+v(ip,jm,2)+v(i,jm,2))/4)
            v(i,j,3) = v(i,j,1) + 2*dt * (-g*(h(i,jp,2)-h(i,j,2))/dy - f*(u(i,j,2)+u(i,jp,2)+u(im,jp,2)+u(im,j,2))/4)

            END DO
        END DO

        ! DO an Asselin-filter
        h(:,:,2) = h(:,:,2) + alpha * (h(:,:,1) - 2*h(:,:,2) + h(:,:,3))
        u(:,:,2) = u(:,:,2) + alpha * (u(:,:,1) - 2*u(:,:,2) + u(:,:,3))
        v(:,:,2) = v(:,:,2) + alpha * (v(:,:,1) - 2*v(:,:,2) + v(:,:,3))


        ! Shift time levels
        h(:,:,1) = h(:,:,2)
        h(:,:,2) = h(:,:,3)

        u(:,:,1) = u(:,:,2)
        u(:,:,2) = u(:,:,3)

        v(:,:,1) = v(:,:,2)
        v(:,:,2) = v(:,:,3)

        write(10, *) h(:,:,2) ! Save

    END DO

    close(10)

    print *, "Simulation completed, saved as: ", filename 

END PROGRAM Cgrid