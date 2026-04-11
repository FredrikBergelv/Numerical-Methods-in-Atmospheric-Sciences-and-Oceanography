PROGRAM leapfrog

    implicit none

    real, parameter :: CFL = 0.9

    real, parameter :: delX=0.02, c=1.0, gamma=0
    real, parameter :: delT = CFL * delX / c
    real, parameter :: Lx=1.0, Lt=2.0, pi = 4.0 * ATAN(1.0)
    integer, parameter :: Nx = INT(Lx/delX), Nt = INT(Lt/delT)

    integer :: j, n
    real :: x
    real(8), dimension(Nt, Nx) :: array
    character(len=50) :: filename


    ! initialize
    DO j = 1, Nx
        x = (j-1)*delX
        if (x<0.6 .AND. x>0.4) then
            array(1,j) = 0.5 + 0.5*cos(10*pi*(x-0.5))
        else 
            array(1,j) = 0
        end if
    END DO

    ! create one more step wit forward Euler
    DO j = 1, Nx-1
        if (j == 1) then
            array(2,j) = array(1,j) - 0.5*CFL * (array(1,j+1) - array(1,Nx))
        else if (j == Nx) then
            array(2,j) = array(1,j) - 0.5*CFL * (array(1,1) - array(1,j-1))
        else
            array(2,j) = array(1,j) - 0.5*CFL * (array(1,j+1) - array(1,j-1))
        end if
    END DO


    ! travelling wave
    DO n = 2, Nt-2
        DO j = 1, Nx
            if (j == 1) then 
                array(n+1,j)= array(n-1,j) - CFL * (array(n,j+1) - array(n,Nx))

            else if (j == Nx) then
                array(n+1,j)= array(n-1,j) - CFL * (array(n,1) - array(n,j-1))

            else                               
                array(n+1,j)= array(n-1,j) - CFL * (array(n,j+1) - array(n,j-1))
            end if 
            array(n,j)= array(n,j) +gamma * (array(n-1,j) - 2*array(n,j) + array(n+1,j))
        END DO
    END DO



    ! write file
    write(filename, '(A,F4.2,A)') 'leapfrog_CFL_', CFL, '.txt'    
    open(10, file=filename, status="replace")
    do n = 1, Nt
        write(10, *) array(n, :)
    end do
    close(10)



END PROGRAM leapfrog