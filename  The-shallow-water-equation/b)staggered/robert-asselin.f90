PROGRAM asselin

    implicit none

    real, parameter :: CFL = 0.45

    real, parameter :: dx=0.025, c=1.0, g=1.0, H=1.0, gamma=0.005
    real, parameter :: dt = CFL * dx / c
    real, parameter :: Lx=1.0, Lt=10.0, pi = 4.0 * ATAN(1.0)
    integer, parameter :: Nx = INT(Lx/dx), Nt = INT(Lt/dt)

    integer :: j, n
    real :: x
    real(8), dimension(Nt, Nx) :: h_array
    real(8), dimension(Nt, Nx) :: u_array

    character(len=50) :: filename


    ! initialize
    u_array = 0.0
    DO j = 1, Nx
        x = (j-1)*dx
        if (x<0.6 .AND. x>0.4) then
            h_array(1,j) = 0.5 + 0.5*cos(10*pi*(x-0.5))
        else 
            h_array(1,j) = 0
        end if
    END DO

    ! create one step with forward Euler
    DO j = 1, Nx
        if (j == 1) then
            h_array(2,j) = h_array(1,j) - (H*dt/(dx)) * (u_array(1,j) - u_array(1,Nx))
            u_array(2,j) = u_array(1,j) - (g*dt/(dx)) * (h_array(1,j+1) - h_array(1,1))

        else if (j == Nx) then
            h_array(2,j) = h_array(1,j) - (H*dt/(dx)) * (u_array(1,Nx) - u_array(1,Nx-1))
            u_array(2,j) = u_array(1,j) - (g*dt/(dx)) * (h_array(1,1) - h_array(1,Nx))

        else
            h_array(2,j) = h_array(1,j) - (H*dt/(dx)) * (u_array(1,j) - u_array(1,j-1))
            u_array(2,j) = u_array(1,j) - (g*dt/(dx)) * (h_array(1,j+1) - h_array(1,j))
        end if
    END DO


    ! travelling wave
    DO n = 2, Nt-1
        DO j = 1, Nx
            if (j == 1) then 
                h_array(n+1,j) = h_array(n-1,j) - 2*(H*dt/(dx)) * (u_array(n,1) - u_array(n,Nx))
                u_array(n+1,j) = u_array(n-1,j) - 2*(g*dt/(dx)) * (h_array(n,j+1) - h_array(n,1))

            else if (j == Nx) then
                h_array(n+1,j) = h_array(n-1,j) - 2*(H*dt/(dx)) * (u_array(n,Nx) - u_array(n,j-1))
                u_array(n+1,j) = u_array(n-1,j) - 2*(g*dt/(dx)) * (h_array(n,1) - h_array(n,j))

            else                               
                h_array(n+1,j) = h_array(n-1,j) - 2*(H*dt/(dx)) * (u_array(n,j) - u_array(n,j-1))
                u_array(n+1,j) = u_array(n-1,j) - 2*(g*dt/(dx)) * (h_array(n,j+1) - h_array(n,j))
            end if 
        END DO

        DO j = 1, Nx
            h_array(n,j) = h_array(n,j) + gamma * (h_array(n-1,j) - 2*h_array(n,j) + h_array(n+1,j))
            u_array(n,j) = u_array(n,j) + gamma * (u_array(n-1,j) - 2*u_array(n,j) + u_array(n+1,j))
        END DO

    END DO



    ! write files
    write(filename, '(A,F5.4,A)') 'b)staggered/h-leapfrog-robert-asselin.txt'    
    open(10, file=filename, status="replace")
    do n = 1, Nt
        write(10, *) h_array(n, :)
    end do
    close(10)

    print *, "Simulation completed. Results written to ", filename


END PROGRAM asselin