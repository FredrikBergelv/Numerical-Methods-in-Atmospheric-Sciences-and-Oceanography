PROGRAM leapfrog
    implicit none

    call CreateMovementFiles(0.9)
    call CreateMovementFiles(1.0)
    call CreateMovementFiles(1.1)

CONTAINS

    subroutine CreateMovementFiles(CFL)
        implicit none

        real, intent(in) :: CFL
        real, parameter :: delX=0.02, c=1.0
        real, parameter :: Lx=1.0, Lt=2.0, pi = 4.0 * ATAN(1.0)

        real :: delT
        integer :: Nx, Nt
        integer :: j, n
        real :: x
        real, allocatable :: array(:,:)
        character(len=50) :: filename

        ! compute runtime values
        delT = CFL * delX / c
        Nx = INT(Lx/delX)
        Nt = INT(Lt/delT)

        allocate(array(Nt, Nx))

        ! initialize
        DO j = 1, Nx
            x = (j-1)*delX
            array(1,j) = cos(2*pi*x)
        END DO

        ! forward Euler first step
        DO j = 1, Nx
            if (j == 1) then
                array(2,j) = array(1,j) - 0.5*CFL * (array(1,j+1) - array(1,Nx))
            else if (j == Nx) then
                array(2,j) = array(1,j) - 0.5*CFL * (array(1,1) - array(1,j-1))
            else
                array(2,j) = array(1,j) - 0.5*CFL * (array(1,j+1) - array(1,j-1))
            end if
        END DO

        ! leapfrog
        DO n = 2, Nt-1
            DO j = 1, Nx
                if (j == 1) then 
                    array(n+1,j)= array(n-1,j) - CFL * (array(n,j+1) - array(n,Nx))
                else if (j == Nx) then
                    array(n+1,j)= array(n-1,j) - CFL * (array(n,1) - array(n,j-1))
                else                               
                    array(n+1,j)= array(n-1,j) - CFL * (array(n,j+1) - array(n,j-1))
                end if 
            END DO
        END DO

        ! write file
        write(filename, '(A,F4.2,A)') 'leapfrog_CFL_', CFL, '.txt'
        open(10, file=filename, status="replace")
        do n = 1, Nt
            write(10, *) array(n, :)
        end do
        close(10)

        deallocate(array)

    end subroutine CreateMovementFiles

END PROGRAM leapfrog