PROGRAM Cgrid

    implicit none

    ! Namelist parameters 
    real :: CFL, f, dx, dy, g, H0, Lx, Ly, Lt, gamma
    namelist /params/ CFL, f, dx, dy, g, H0, Lx, Ly, Lt, gamma

    ! VOLariables 
    real :: dt
    integer :: Nx, Ny, Nt
    real :: xc, yc, r, r2

    integer :: i, j, n, ip, im, jp, jm
    real :: x, y
    real(8), allocatable :: h(:,:,:), u(:,:,:), v(:,:,:)
    character(len=100) :: filename
    real, parameter :: pi = 4.0 * atan(1.0)
    integer :: savefreq = 20
    real(8) :: VOL, EP, EK

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

    ! Open file for saving
    filename = "2D-SWE/h_array_wall.txt"
    open(10, file=filename, status="replace")

    open(20, file="2D-SWE/energy.txt", status="replace")


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

            xc = 0.5*Lx
            yc = 0.5*Ly
            r  = sqrt( (x - xc)**2 + (y - yc)**2 )

            r2 = (x - xc)**2 + (y - yc)**2

            if (r < 0.3*Lx) then
                h(i,j,1) = 20.0 * exp(-r2 / (0.01*Lx*Lx))
            else
                h(i,j,1) = 0.0
            end if
        end do
    END DO

    write(10, *) h(:,:,1) ! Save

    call compute_energy(h(:,:,1), u(:,:,1), v(:,:,1), dx, dy, H0, g, VOL, EP, EK)
    write(20, *) n*dt, VOL, EP, EK


    ! First step (Forward Euler)
    DO j = 1, Ny
        DO i = 1, Nx

            ! WALL BOUNDARIES 
            ip = i + 1
            im = i - 1
            jp = j + 1
            jm = j - 1

            if (i == Nx) ip = i
            if (i == 1)  im = i
            if (j == Ny) jp = j
            if (j == 1)  jm = j

            ! Do the Euler forward 
            h(i,j,2) = h(i,j,1) - H0*dt * ((u(i,j,1)-u(im,j,1))/dx + (v(i,j,1)-v(i,jm,1))/dy)

            u(i,j,2) = u(i,j,1) + dt * ( &
                -g*(h(ip,j,1)-h(i,j,1))/dx + &
                 f*(v(i,j,1)+v(ip,j,1)+v(ip,jm,1)+v(i,jm,1))/4 )

            v(i,j,2) = v(i,j,1) + dt * ( &
                -g*(h(i,jp,1)-h(i,j,1))/dy - &
                 f*(u(i,j,1)+u(i,jp,1)+u(im,jp,1)+u(im,j,1))/4 )

        END DO
    END DO

    !write(10, *) h(:,:,2) ! Save


    ! Enforce wall BC
    DO j = 1, Ny
        DO i = 1, Nx

            if (i == 1 .or. i == Nx) then
                u(i,j,1) = 0.0
                u(i,j,2) = 0.0
                u(i,j,3) = 0.0
            end if

            if (j == 1 .or. j == Ny) then
                v(i,j,1) = 0.0
                v(i,j,2) = 0.0
                v(i,j,3) = 0.0
            end if

        END DO
    END DO


    ! Leapfrog time stepping
    DO n = 2, Nt-1

        DO j = 1, Ny
            DO i = 1, Nx

                ! WALL BOUNDARIES 
                ip = i + 1
                im = i - 1
                jp = j + 1
                jm = j - 1

                if (i == Nx) ip = i
                if (i == 1)  im = i
                if (j == Ny) jp = j
                if (j == 1)  jm = j

                ! Leapfrog scheme
                h(i,j,3) = h(i,j,1) - 2*H0*dt * ((u(i,j,2)-u(im,j,2))/dx + (v(i,j,2)-v(i,jm,2))/dy)

                u(i,j,3) = u(i,j,1) + 2*dt * ( &
                    -g*(h(ip,j,2)-h(i,j,2))/dx + &
                     f*(v(i,j,2)+v(ip,j,2)+v(ip,jm,2)+v(i,jm,2))/4 )

                v(i,j,3) = v(i,j,1) + 2*dt * ( &
                    -g*(h(i,jp,2)-h(i,j,2))/dy - &
                     f*(u(i,j,2)+u(i,jp,2)+u(im,jp,2)+u(im,j,2))/4 )
            
            END DO
        END DO

        ! Asselin filter
        h(:,:,2) = h(:,:,2) + gamma * (h(:,:,1) - 2*h(:,:,2) + h(:,:,3))
        u(:,:,2) = u(:,:,2) + gamma * (u(:,:,1) - 2*u(:,:,2) + u(:,:,3))
        v(:,:,2) = v(:,:,2) + gamma * (v(:,:,1) - 2*v(:,:,2) + v(:,:,3))

        ! Shift time levels
        h(:,:,1) = h(:,:,2)
        h(:,:,2) = h(:,:,3)

        u(:,:,1) = u(:,:,2)
        u(:,:,2) = u(:,:,3)

        v(:,:,1) = v(:,:,2)
        v(:,:,2) = v(:,:,3)



        ! Enforce wall BC 
        DO j = 1, Ny
            DO i = 1, Nx
                if (i == 1 .or. i == Nx) then
                    u(i,j,1:3) = 0.0
                end if
                if (j == 1 .or. j == Ny) then
                    v(i,j,1:3) = 0.0
                end if
            END DO
        END DO

        if (mod(n,savefreq) == 0) then
            write(10, *) h(:,:,2)

        end if 

        call compute_energy(h(:,:,2), u(:,:,2), v(:,:,2), dx, dy, H0, g, VOL, EP, EK)
            write(20, *) n*dt, VOL, EP, EK

        !print*, "t = ", n*dt

    END DO

    close(10)
    close(20)


    
    print *, "Simulation completed, saved as: ", filename

        write(*,'(A,I0)') "Nx = ", Nx
        write(*,'(A,I0)') "Ny = ", Ny
        write(*,'(A,I0)') "Lt = ", int(Lt)
        write(*,'(A,I0)') "Lx = ", int(Lx)
        write(*,'(A,I0)') "Ly = ", int(Ly)
        write(*,'(A,I0)') "stride = ", savefreq


        


    contains

    subroutine compute_energy(hin, uin, vin, dx_s, dy_s, H0_s, g_s, VOL_s, EP_s, EK_s)

        implicit none

        real, intent(in) :: dx_s, dy_s, H0_s, g_s

        real(8), intent(in) :: hin(Nx,Ny), uin(Nx,Ny), vin(Nx,Ny)

        real(8), intent(out) :: VOL_s, EP_s, EK_s

        integer :: i_s, j_s

        VOL_s  = 0.0d0
        EP_s = 0.0d0
        EK_s = 0.0d0

        !print*, maxval(hin(:,:))
        
        do j_s = 1, Ny
            do i_s = 1, Nx

                VOL_s  = VOL_s  + hin(i_s,j_s) * dx_s * dy_s
                EP_s = EP_s + 0.5d0 * g_s  * hin(i_s,j_s)**2 * dx_s * dy_s
                EK_s = EK_s + 0.5d0 * H0_s * (uin(i_s,j_s)**2 + vin(i,j)**2) * dx_s * dy_s



            end do
        end do

    end subroutine compute_energy

END PROGRAM Cgrid